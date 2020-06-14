# coding=utf-8
# Author: weitingtao
# File: urls.py.py
# Create_time: 2019/10/18 22:08

from django.urls import path, re_path
from . import views


app_name = 'pychen_login'
urlpatterns = [
    re_path(r'^login/$', views.pychen_login, name='pychen_login'),
]