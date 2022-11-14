from django.db import models

class User(models.Model):
    username = models.CharField(max_length=70, blank=False, default='')
    password = models.CharField(max_length=25, blank=False, default='')
    email = models.CharField(max_length=25, blank=False, default='')
    first_name = models.CharField(max_length=25, blank=False, default='')

