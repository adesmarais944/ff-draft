from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('players/', views.players, name='players'),
    path('teams/', views.teams, name='teams'),
    path('drafts/', views.drafts, name='drafts'),
    path('view/', views.view, name='view'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]