from django.db import models
from django.contrib.auth.models import User
import requests
import os

class Hero(models.Model):
    name = models.CharField(max_length=30)
    hero_id = models.CharField(max_length=10,unique=True)
    imageUrl = models.URLField(max_length=200)

    def __str__(self):
        return self.name
