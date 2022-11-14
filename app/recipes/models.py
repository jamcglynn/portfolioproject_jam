from django.db import models

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=70, blank=False, default='')
    recipe_instructions = models.CharField(max_length=65535, blank=False, default='')
    published = models.BooleanField(default=False)

