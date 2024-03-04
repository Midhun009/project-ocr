from django.urls import path
from core import views
from django.contrib import admin

urlpatterns = [
    path('', views.upload_image, name='upload_image'),
    path('admin/', admin.site.urls),
    # Add other URL patterns here if needed
]
