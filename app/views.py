from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from taggit.models import Tag

from .forms import EmailPostForm, CommentForm
from .models import Post, Comment


def post_list(request, tag_slug=None):
    obj_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        obj_list = obj_list.filter(tags__in=[tag])

    paginator = Paginator(object_list=obj_list, per_page=2)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        template_name="blog/post/list.html",
        context={
            "page": page,
            "posts": posts,
            "tag": tag
        }
    )


def post_detail(request, year: int, month: int, day: int, post_msg: str):
    post = get_object_or_404(
        Post,
        slug=post_msg,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    comment_form = None
    new_comment = None

    if request.method == "POST":
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object, but don't save to db yet.
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            new_comment.save()
        else:
            comment_form = CommentForm()

    return render(
        request,
        template_name="blog/post/detail.html",
        context={
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form
        }
    )


# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = "posts"
#     paginate_by = 2
#     template_name = "blog/post/list.html"


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status="published"
    )
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(
                subject=subject,
                message=message,
                from_email="julesc003@gmail.com",
                recipient_list=[cd["to"]]
            )
            sent = True

    else:
        form = EmailPostForm()

    return render(
        request,
        template_name="blog/post/share.html",
        context={
            "post": post,
            "form": form,
            "sent": sent
        }
    )


