from django.urls import path
from . import views


urlpatterns = [
    path('hot/', views.getHot, name='hot'),
    path('<int:cerid>/', views.getCer, name='get'),
]