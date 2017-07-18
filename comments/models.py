# coding:utf-8
from django.db import models
from django.utils.six import python_2_unicode_compatible
# Create your models here.

@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    # auto_now_add 的作用是，
    # 当评论数据保存到数据库时，自动把 created_time 的值指定为当前时间。

    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ["-created_time"]
