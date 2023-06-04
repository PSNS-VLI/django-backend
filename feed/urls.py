from django.urls import path
from .views import *

urlpatterns = [
    # 旧版本接口已废弃
    # path("post", post_hot, name="post_hot"),
    path("post", post_feed, name="post_feed"),
    # path("get", get_hot, name="get_hot"),
    # path("gettable", get_hot_table, name="get_hot_table"),
    path("gettable", get_feed_table, name="get_feed_table"),
    path("get", get_feed, name="get_feed"),
    path("search", search_feed, name="gsearch_feed"),
    path("news/post", post_news, name="post_new"),
    path("news/get", get_news, name="get_new"),
    path("news/gettable", get_news_table, name="get_new_table"),
]