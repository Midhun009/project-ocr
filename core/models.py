from django.db import models

class BusinessCard(models.Model):
    filename = models.CharField(max_length=255,blank=True, null=True) 
    company_name = models.CharField(max_length=255,blank=True, null=True) 
    phone = models.CharField(max_length=20,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)    
    website = models.URLField(blank=True, null=True)    

    def __str__(self):
        return f'{self.company_name}'
