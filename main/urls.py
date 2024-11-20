from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("players/", views.player_data, name="player_data")
]