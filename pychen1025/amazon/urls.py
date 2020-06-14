# coding=utf-8
# Author: weitingtao
# File: urls.py
# Create_time: 2019/10/19 19:56

from django.urls import path
from . import views


app_name = 'amazon'
urlpatterns = [
    path('home/', views.home, name='主页'),
    path('chart/', views.chart, name='折线图'),
    path('collect/<asin>', views.collect, name='收藏'),
    path('alibaba/<asin>', views.alibaba, name='1688'),
    path('monitor/<asin>', views.monitor, name='监测'),
    path('readInfo/<update_time>', views.readInfo, name='阅读进度'),
]
