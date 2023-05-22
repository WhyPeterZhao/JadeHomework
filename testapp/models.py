from django.db import models
from django.http import *
from haystack import indexes
from haystack.views import SearchView

# Create your models here.

class User(models.Model):
    # 创建模型类并继承models.Model
    # 一个类就是数据库的一张表（本案例中叫User表）
    gender = (
        ('male',"男"),   # 二维元素数组，第一个值为数据库中存储的值，第二个值是html页面上显示的值
        ('female',"女"),
    )
    name=models.CharField(max_length=128,unique=True)   # 最多128个字符，在数据库中唯一（不能出现重复用户名）
    password=models.CharField(max_length=256)           # 密码最长256个字符
    email=models.EmailField(unique=True)                # 邮箱必须是唯一的
    sex=models.CharField(max_length=32,choices=gender,default='男')  # 可选择，默认为男
    c_time=models.DateTimeField(auto_now_add=True)      # 记录注册时间
    is_staff=models.BooleanField('active',default=0)    # 是否激活

    def __str__(self):
        return self.name

    class Meta: # 为这个类定义一个说明
        ordering=["-c_time"]
        verbose_name="用户"           # 设置对象名称，若没有设置，则默认为该类名的小写分词形式
        verbose_name_plural="用户"    # 设置对象名称复数（例如usercms），一般设置跟verbose_name一样
                                     # 不加这个的话在我们的verbose_name在admin里面会被自动加上s



# 邮箱验证码字段
class EmailVerifyRecord(models.Model):
    SEND_TYPE_CHOICES = (
        ('register', '注册账号'),
        ('forget', '找回密码'),
    )
    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField(choices=SEND_TYPE_CHOICES, max_length=10, default='register')
    send_time = models.DateTimeField('时间', auto_now_add=True)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code

# 视频文件的数据表
class Video(models.Model):
    title=models.CharField('视频名',max_length=150,unique=True)   # 最多150个字符，在数据库中不唯一，视频可以重名
    cover_url = models.URLField('封面url',max_length=500)         # 视频封面url
    video_url = models.URLField('视频url',max_length=500)         # 视频文件url
    duration = models.DurationField('视频时长')                    # 视频时长
    profile = models.TextField('视频简介', null=True, blank=True)  # 视频简介

    class Meta:
        verbose_name="视频"           # 设置对象名称，若没有设置，则默认为该类名的小写分词形式
        verbose_name_plural=verbose_name    # 设置对象名称复数（例如usercms），一般设置跟verbose_name一样

    def __str__(self):
        return self.title

class Comment(models.Model):
    # video和comment_time均为外键，关联相关视频和评论人
    video = models.ForeignKey(to=Video, on_delete=models.DO_NOTHING, verbose_name='评论视频')
    comment_content = models.TextField(verbose_name='评论内容')
    comment_author = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, verbose_name='评论者')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    is_valid=models.BooleanField(default=False,verbose_name='是否通过审核')
    #设置严格的审核机制，管理员在后台人工审核后方可展示评论

    class Meta:
        db_table = 'comment_tb'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
