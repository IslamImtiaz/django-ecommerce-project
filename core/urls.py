# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('set_currency/', views.set_currency, name='set_currency'),
]