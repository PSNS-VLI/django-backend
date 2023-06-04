from django.urls import path
from .views import *

urlpatterns = [
    path("get/feedcomment", get_feed_comment, name="get_feed_comment"),
    path("post/feedcomment", post_feed_comment, name="post_feed_comment"),
]