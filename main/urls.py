from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("players/", views.players, name="players"),
    path("teams/", views.teams, name="teams"),
    path("drafts/", views.drafts, name="drafts")
]