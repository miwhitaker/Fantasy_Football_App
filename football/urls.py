from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.fantasy, name = 'fantasy'),
    path('fantasy', views.fantasy, name = 'fantasy'),
    path('draft', views.draft, name = "draft"),
    path('team', views.team, name = 'team'),
    path('standings', views.standings, name = 'standings'),
    path('matchup', views.matchup, name = 'matchup'),
    path('lobby', views.lobby, name = "lobby"),
]