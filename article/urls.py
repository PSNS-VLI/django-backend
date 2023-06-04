from django.urls import path
from .views import *


urlpatterns = [
    path('recommend', recommend_article, name='recommend'),
    path('get', get_article, name='recommend')
]