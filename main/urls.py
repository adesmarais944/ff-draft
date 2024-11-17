from django.urls import path

from . import views

urlpatterns = [
    path("", views.player_data, name="index")
]