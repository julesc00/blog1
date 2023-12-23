
from django.urls import path
from .views import (PostListView, post_detail)  # post_list,

app_name = "blog"

urlpatterns = [
    # path("", post_list, name="post_list"),
    path("", PostListView.as_view(), name="post_list"),
    path("<int:year>/<int:month>/<int:day>/<slug:post_msg>", post_detail, name="post_detail"),
]
