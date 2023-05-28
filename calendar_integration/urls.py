from django.contrib import admin
from django.urls import path
from .views import hello

urlpatterns = [
    path('/init', hello),
]
