from django.urls import path
from .views import *

urlpatterns = [
    path("history/post", post_history, name="post_history"),
    path("history/get", get_history, name="get_history"),
    path("collect/post", post_collect, name="post_collect"),
    path("collect/get", get_collect, name="get_collect"),
    path("like/post", post_like, name="post_like"),
    path("comment_like/post", post_comment_like, name="post_comment_like"),
]