from django.db import models

# Create your models here.
class User(models.Model):
    sell_list = models.CharField(max_length=500)
    watch_list = models.CharField(max_length=500)
    email = models.CharField(max_length=100)
