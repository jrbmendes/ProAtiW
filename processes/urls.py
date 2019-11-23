"""
Definition of urls for estimpal.
"""

from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from processes import views

app_name = 'processes'

urlpatterns = [ 
    path('structureView/<int:activity_id>', views.structureView, name='structureView'), 
 ]
