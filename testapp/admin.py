from django.contrib import admin

# Register your models here.

from.import models

admin.site.register(models.User)

# 注册EmailVerifyRecord类，实现在django的admin中管理验证码
from .models import EmailVerifyRecord

@admin.register(EmailVerifyRecord)
class EamilVerifyRecordAdmin(admin.ModelAdmin):
    '''Admin View for EamilVerifyRecord'''
    list_display = ('code',)

# 注册video表
from .models import Video
admin.site.register(models.Video)

# 注册评论表
from .models import Comment
admin.site.register(models.Comment)