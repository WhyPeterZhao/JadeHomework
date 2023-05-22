"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from testapp import views
from django.conf.urls import include
from testapp import models

urlpatterns = [
    # 管理后台页面
    path("admin/", admin.site.urls),
    # 主页&登录&注册页面+登出操作
    path('index/',views.index),
    path('login/',views.login),
    path('register/',views.register),
    path('logout/',views.logout),
    path('active/<active_code>/',views.active_user),
    path('video/<course_id>/', views.video.as_view(), name='video_sign'),
    path('comment_control/',views.comment_control),
    path('search/', views.MySearchView(), name='haystack_search'),
]
