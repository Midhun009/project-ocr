from django.urls import path
from core import views
from django.contrib import admin

urlpatterns = [
        path('', views.capture_image, name='capture_image'),
    # Add other URL patterns here if needed
]
