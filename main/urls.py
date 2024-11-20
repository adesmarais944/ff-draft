from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("players/", views.player_data, name="player_data"),
    path("players2/", views.player_data2, name="player_data2")
]