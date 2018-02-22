#coding:utf-8

from haystack import indexes
from .models import Post


'''
该文件目的是：创建索引
要相对某个 app 下的数据进行全文检索，就要在该 app 下创建一个 search_indexes.py 文件，然后创建一个 XXIndex 类

'''
class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # haystack 提供了use_template=True 在 text 字段中，这样就允许我们使用数据模板去建立搜索引擎索引的文件，说得通俗点就是索引里面需要存放一些什么东西

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()