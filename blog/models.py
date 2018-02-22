#_*_coding:utf-8_*_

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

import markdown
from django.utils.html import strip_tags


class Category(models.Model):
    # 分类表
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    # 标签表
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    # 文章表
    title = models.CharField(max_length=70)

    body = models.TextField()

    created_time = models.DateTimeField()

    modified_time = models.DateTimeField()

    excerpt = models.CharField(max_length=200, blank=True)

    category = models.ForeignKey(Category)

    tags = models.ManyToManyField(Tag, blank=True)

    author = models.ForeignKey(User)

    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
    '''
    如果 Post 的 id（或者 pk，这里 pk 和 id 是等价的） 是 255 的话，
    那么 get_absolute_url 函数返回的就是 /post/255/ ，这样 Post 自己就生成了自己的 URL
    '''
    def get_absolute_url(self):  # 该方法是用post对象  取得   包含post-id的“URL”
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=["views"])  # 注意这里使用了 update_fields 参数来告诉 Django 只更新数据库中 views 字段的值，以提高效率。

    def save(self, *args, **kwargs):
        # 如果没有摘要的
        if not self.excerpt:
            # 实例化一个markdown类，来渲染body的文本
            md = markdown.Markdown(extensions=[
             'markdown.extensions.extra',
             'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    # 这样指定以后所有返回的文章列表都会自动按照 Meta 中指定的顺序排序
    class Meta:
        ordering = ["-created_time"]






