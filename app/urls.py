# lfc_teens/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-like/', views.add_like, name='add_like'),
]