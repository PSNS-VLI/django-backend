"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from .consumers import ChatConsumer
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='index/')),
    path('erp/', TemplateView.as_view(template_name='index_erp.html')),
    path('admin/', admin.site.urls),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('index/', include(('index.urls', 'index'), namespace='index')),
    path('certificate/', include(('certificate.urls', 'certificate'), namespace='certificate')),
    path('feed/', include(('feed.urls', 'feed'), namespace='feed')),
    path('topic/', include(('topic.urls', 'topic'), namespace='topic')),
    path('comment/', include(('comment.urls', 'comment'), namespace='comment')),
    path('log/', include(('log.urls', 'comment'), namespace='log')),
    path('photo/', include(('photo.urls', 'photo'), namespace='photo')),
    path('apply/', include(('apply.urls', 'apply'), namespace='apply')),
    path('article/', include(('article.urls', 'article'), namespace='article')),
    path('notice/', include(('notice.urls', 'notice'), namespace='notice')),
    re_path('media/(?P<path>.*)', serve,
            {'document_root': settings.MEDIA_ROOT}, name='media'),
    re_path('static/(?P<path>.*)', serve,
            {'document_root': settings.STATIC_ROOT}, name='static'),
    path("*", TemplateView.as_view(template_name='index_erp.html'))
]

websocket_patterns = [
    path('ws/chat/<room_name>/', ChatConsumer),
]

handler404 = 'index.views.pag_not_found'
