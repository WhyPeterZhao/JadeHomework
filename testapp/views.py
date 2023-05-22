from django.shortcuts import render
from django.shortcuts import redirect
from testapp.models import User
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from  django.conf import settings
from django.views.generic import View
from django.shortcuts import Http404
from captcha.models import CaptchaStore
from django.http import JsonResponse
from captcha.helpers import  captcha_image_url
from django.contrib import auth         #使用Django的auth认证组件
from django.db.models import Q
import json
import hashlib
import re
from utils.email_send import send_register_email
from .models import EmailVerifyRecord  # 创建邮箱验证记录的类
from .models import Video
from .models import Comment

# Create your views here.

# 限制登录，只有登录的用户才能访问网站主页 -> 使用装饰器
def userValid(fun):
    def inner(request, *args, **kwargs):
        name = request.COOKIES.get("name")
        if name:
            print(name)
            return fun(request, *args, **kwargs)
        else:
            print('name not found')
            return HttpResponseRedirect('/login/')
    return inner
# Index主页页面请求

@userValid
def index(request):
    return render(request, "testapp/index.html")

# login登录页面请求
def login(request):
    if request.method == 'POST' and request.POST:
        name = request.POST.get("name")
        password = request.POST.get("password")
        e = User.objects.filter(name=name).first()
        if not e:
            e = User.objects.filter(email=name).first()
        error_name = ""
        if e:
            print("def login:get user"+str(e.name))
            now_password = setPassword(password)
            db_password = e.password
            if not e.is_staff:
                print("def login:not active")
                error_name = "【用户尚未通过邮箱验证】"  # 密码错误页面
                return render(request, "testapp/login.html", {'error_msg': error_name})
            if now_password == db_password:     # 用户输入的密码正确
                print("def login:password correct")
                response = HttpResponseRedirect('/index/')
                print(e.id)
                print(request.user.id)
                response.set_cookie("id",e.id)
                response.set_cookie("name", e.name)     # 设置浏览器携带的cookie值
                return response
            else:
                print("def login:password incorrect")
                error_name="【密码错误】"    # 密码错误页面
                return render(request, "testapp/login.html", {'error_msg': error_name})
        else:
            print("def login:user invalid")
            error_name="【用户不存在】"    # 用户不存在页面
            return render(request, "testapp/login.html", {'error_msg': error_name})
    else:
        print("def login:request invalid")
        pass    # 数据请求无效页面
        return render(request, "testapp/login.html")

# 密码md5单词加密函数，在register和login中调用
def setPassword(password):
    md5 = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))  # md5实例化 加盐防止撞库
    md5.update(password.encode("utf-8"))
    password = md5.hexdigest()
    print("def setPassword:md5 operation complete")
    return str(password)

# 正则表达式匹配
# 检测用户名（只能有英文字符、下划线、中划线、数字中的一个或多个，并且以字母或数字开头）
def nameInvalid(name):
    s = str(name)
    if re.match('^[0-9a-zA-Z]+$', s[0]) and re.match('^[0-9a-zA-Z_-]+$', s[1:]):
        return True
    else:
        return False

# 检测密码（只能有英文字符和数字）
def passwordInvalid(password):
    zhmodel = re.compile(u'[\u4e00-\u9fa5]')
    res = zhmodel.search(password)
    if len(password)<8:  # 检查密码长度是否符合要求
        return False
    if res:              # 检查是否有中文
        return False
    if password.isdigit() or password.isalnum() and not zhmodel.search(password):
        return True      # 只有英文和数字

# register注册页面请求函数
def register(request):
    if request.method == "POST" and request.POST:   # 点击注册按钮即可开始POST（post类型的请求表示上传数据）
        data = request.POST     # 请求主题对象
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        error_msg=""    # 报错信息
        print(name)
        e1 = User.objects.filter(name=name).first()
        e2 = User.objects.filter(email=email).first()
        if e1:
            print("def register:username existed")
            error_name = "【用户名已存在】"  # 用户名过短
            return render(request, "testapp/register.html", {'error_msg': error_name})
        elif len(name)==0:
            print("def register:username too short")
            error_name = "【用户名不能为空】"  # 用户名过短
            return render(request, "testapp/register.html", {'error_msg': error_name})
        elif not nameInvalid(name):
            print("def register:username invalid")
            error_name="【用户名非法，请查看命名规范】"    # 用户名无效
            return render(request, "testapp/register.html",{'error_msg':error_name})
        elif e2:
            print("def register:email existed")
            error_name = "【该邮箱地址已注册过帐号】"  # 用户名过短
            return render(request, "testapp/register.html", {'error_msg': error_name})
        elif not passwordInvalid(password):
            print("def register:password invalid")
            error_name="【密码格式错误】"  # 密码格式错误
            return render(request, "testapp/register.html",{'error_msg':error_name})
        User.objects.create(
            name=name,
            email=email,
            password=setPassword(password),
        )
        send_register_email(email,'register')
        print("def register:register "+name+" succeed")
        e = User.objects.filter(name=name).first()
        return HttpResponseRedirect('/login/')
    else:
        print("def register:request invalid")
        return render(request, "testapp/register.html")

# logout退出登录页面请求（回到登陆页面，删除登录信息）
def logout(request):
    response=HttpResponseRedirect('/login/')
    response.delete_cookie("username")
    return response

# 邮箱验证码查询函数
def active_user(request, active_code):
    """查询验证码"""
    print("enter-and-change")
    all_records = EmailVerifyRecord.objects.filter(code=active_code)
    print(all_records)
    if all_records:
        for record in all_records:
            email = record.email
            print(email)
            user = User.objects.get(email=email)
            print(user)
            user.is_staff = 1
            user.save()
    else:
        return HttpResponse('链接有误！')
    return redirect('/login/')

# 主页
def index(request):
    if request.method == "POST" and request.POST:
        data = request.POST  # 请求主题对象
        search=data.get("search")
        print("def index->search="+str(search))
        videos = Video.objects.filter(title=match(search))
    else:
        videos = Video.objects.all()
    # 获取数据
    # 视频渲染
    print('get videos')
    return render(request,'testapp/index.html',context={'videos': videos})

# 视频播放页面
class video(View):
    def get(self, request, course_id):
        print('get reverse-> ')
        print(course_id)
        course = Video.objects.get(id=course_id)
        comment_list = Comment.objects.filter(Q(video_id=course_id)&Q(is_valid=True))  # 从数据库找出该文章的评论数据对象
        if course:
            return render(request, 'testapp/video.html', context={'course': course,'comment_list': comment_list})
        else:
            return Http404('此课程不存在')

# 评论模块函数
def comment_control(request):  # 提交评论的处理函数
    print("Into comment_control")
    comment_content = request.POST.get('comment_content')
    video_id = request.POST.get('video_id')
    author_id = request.COOKIES.get("id")  # 获取当前用户的ID
    id = request.COOKIES.get("id")
    course = Video.objects.get(id=video_id)
    course_id = course.id
    Comment.objects.create(comment_content=comment_content, video_id=course_id,
                           comment_author_id=author_id)  # 将提交的数据保存到数据库中
    comment_list = Comment.objects.filter(video_id=course_id)
    video = list('comment_list')  # 以键值对的形式取出评论对象，并且转化为列表list类型
    return JsonResponse(video, safe=False)  # JsonResponse返回JSON字符串，自动序列化，如果不是字典类型，则需要添加safe参数为False

from haystack.views import SearchView

class MySearchView(SearchView):
    def create_response(self):
        context = super().get_context()
        keyword = self.request.GET.get('q', None)  # 关键字为q
        print("whoosh search: "+str(keyword))
        if not keyword:
            print("no keyword")
            return render(self.request,'testapp/sj.html')
        else:
            data_list = [{"id": i.object.id, "title": i.object.title,
                          "cover_url": i.object.cover_url } for i in
                         context['page'].object_list]
        return render(self.request,'testapp/search.html', {'data_list': data_list,'keyword': keyword})
        #return JsonResponse(data_list, safe=False, json_dumps_params={'ensure_ascii': False})