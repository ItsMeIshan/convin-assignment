from django.urls import path
from . import views

urlpatterns = [
    path('init', views.GoogleCalendarInitView, name='init'),
    path('oauth2callback', views.auth_return, name='callback'),
    path('', views.home, name='home'),
]
