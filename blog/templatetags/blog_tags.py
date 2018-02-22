#coding:utf-8
from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count


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
    # 该函数返回分类列表，记得在顶部引入 count 函数
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    # 获取关联post的tag列表
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)