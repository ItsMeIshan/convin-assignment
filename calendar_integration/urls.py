from django.urls import path
from . import views

urlpatterns = [
    path('init', views.GoogleCalendarInitView, name='init'),
    path('redirect', views.GoogleCalendarRedirectView, name='redirect'),
    # path('', views.home, name='home'),
]
