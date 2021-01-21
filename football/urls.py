from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.fantasy, name = 'fantasy'),
    path('fantasy/', views.fantasy, name = 'fantasy'),
]