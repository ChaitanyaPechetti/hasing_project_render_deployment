from django.db import models

# Create your models here.


class Users(models.Model):
    username = models.CharField(max_length=50,primary_key=True)
    password = models.CharField(max_length=100)
    
