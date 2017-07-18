#coding:utf-8
from django.contrib import admin
from .models import Post, Category, Tag
# Register your models here.


#记得要注册到下面去
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']



# 把表注册到后台系统
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)