#coding:utf-8

from django.conf.urls import url
from . import views



# app_name告诉 Django 这个 urls.py 模块是属于 blog 应用的，这种技术叫做视图函数命名空间。
app_name = "blog"
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name="detail"),
    # (?P<pk>[0-9]+) 这个就是匹配数字的固定写法,pk在这里匹配的post的id，pk在views中作为参数传进detail()
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
]
