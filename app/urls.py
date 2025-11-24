# lfc_teens/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('like-post/', views.like_bible_post, name='like_post'),
]