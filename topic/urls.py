from django.urls import path
from .views import *


urlpatterns = [
    path("get/hot_table", get_hot_table, name="get_hot_table"),
    path("get/search_dynamic", get_search_dynamic, name="get_search_dynamic"),
    path("get/search_recommend", get_search_recommend, name="get_search_recommend"),
]