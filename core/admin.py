from django.contrib import admin
from .models import BusinessCard

# Register your models here
@admin.register(BusinessCard)
class BusinessCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'company_name', 'phone', 'email', 'website')
