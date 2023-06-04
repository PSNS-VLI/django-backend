from django.urls import path
from .views import *


urlpatterns = [
    path('carpool/create', create_carpool, name='carpool_create'),
    path('carpool/delete', delete_carpool, name='carpool_delete'),
    path('carpool/get', get_carpool, name='carpool_get'),
    path('carpool/getpersonal', get_personal, name='carpool_create'),
    path('carpool/join', join_carpool, name='carpool_join'),
    path('carpool/quit', quit_carpool, name='carpool_quit'),
]