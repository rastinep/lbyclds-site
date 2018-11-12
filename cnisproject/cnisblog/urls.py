from django.urls import path, include
from django.conf.urls import url
from . import views
from social_core.utils import setting_name
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
]
