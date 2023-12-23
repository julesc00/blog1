from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Post


# def post_list(request):
#     obj_list = Post.published.all()
#     paginator = Paginator(object_list=obj_list, per_page=2)
#     page = request.GET.get("page")
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#
#     return render(
#         request,
#         template_name="blog/post/list.html",
#         context={
#             "page": page,
#             "posts": posts
#         }
#     )


def post_detail(request, year: int, month: int, day: int, post_msg: str):
    post = get_object_or_404(
        Post,
        slug=post_msg,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    return render(
        request,
        template_name="blog/post/detail.html",
        context={"post": post}
    )


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 2
    template_name = "blog/post/list.html"
