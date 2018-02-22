#coding:utf-8
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from comments.forms import CommentForm
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView
import markdown


# Create your views here.
# ListView 就是从数据库中获取某个模型列表数据的，所以 IndexView 继承 ListView。
class IndexView(ListView):

    model = Post
    template_name = "blog/index.html"
    context_object_name = 'post_list'
    paginate_by = 3
    # ListView 传递了以下和分页有关的模板变量供我们在模板中使用：
    # paginator ，即Paginator的实例。
    # page_obj ，当前请求页面分页对象。
    # is_paginated，是否已分页。只有当分页后页面超过两页时才算已分页。
    # object_list，请求页面的对象列表，和post_list等价。所以在模板中循环文章列表时可以选post_list ，也可以选object_list。

    def get_context_data(self, **kwargs):               # 在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
                                                        # 所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        context = super().get_context_data(**kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagiantion_data(paginator, page, is_paginated) # pagiantion_data()该方面我们下面自定义
        context.update(pagination_data)

        return context  # 注意此时 context 字典中已有了显示分页导航条所需的数据。


    def pagiantion_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

            # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number
        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


# def index(request):
#
#     post_list = Post.objects.all()
#     return render(request, 'blog/index.html', context={
#         "post_list": post_list,
#     })


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        self.object.increase_views() # 将文章阅读量 +1

        return response  # 返回的是一个 HttpResponse 实例


    def get_object(self, queryset=None): # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

        return post


    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)  # Post已经定义了get_absolute_url(),这里就能使用了pk去寻找对应post
#     post.body = markdown.markdown(post.body, extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         'markdown.extensions.toc',
#     ])
#     post.increase_views()  #阅读量自增
#
#     form = CommentForm()
#     comment_list = post.comment_set.all() # post是Comment的外键，所以可以通过
#     context={
#         'post': post,
#         'form': form,
#         'comment_list': comment_list
#     }
#     return render(request, 'blog/detail.html', context=context)


class ArchivesView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "post_list"

    def get_queryset(self):
        return super(ArchivesView, self).get_queryset().filter(created_time__year=self.kwargs.get("year"), created_time__month=self.kwargs.get("month"))


# def archives(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class CategoryView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "post_list"

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get("pk")) # 返回的是category对象
        return super(CategoryView, self).get_queryset().filter(category=cate)  # 返回的是某个category下的所有post列表

# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={
#         "post_list": post_list,
#     })


class TagView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "post_list"

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get("pk"))
        return super(TagView, self).get_queryset().filter(tags=tag) # 返回的是某个tag下的所有post列表


def search(request):
    q = request.GET.get("q")
    error_msg = ""

    if not q:
        error_msg = "请输入搜索内容"
        return render(request, 'blog/index.html', {'error_msg': error_msg} )

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {"post_list":post_list, "error_msg":error_msg})
