from django.urls import path
from .views import *


urlpatterns = [
    path('getlist', get_notice_list, name='getlist'),
    path('getnum', get_notice_num, name='getnum'),
    path('get', get_notice, name='get'),
]