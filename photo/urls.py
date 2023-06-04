from django.urls import path
from .views import *


urlpatterns = [
    path('get/feedpicture', get_feed_picture, name='get_feed_picture'),
]