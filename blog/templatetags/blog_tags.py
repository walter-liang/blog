#coding:utf-8
from ..models import Post, Category
from django import template


register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by("-created_time")[:num]
# 定义好上面那个函数后，就可以在模板中用{% get_recent_posts %}的方式 来实现python语句的效果 --{% load blog_tags %}


@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

# 这里 dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）的创建时间，
# 且是 Python 的 date 对象，精确到月份，降序排列。


@register.simple_tag
def get_categories():
    return Category.objects.all()


