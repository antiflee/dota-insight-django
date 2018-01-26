from django.db import models
from django.contrib.auth.models import User
import requests
import os

class Cluster(models.Model):
    cluster_id = models.IntegerField(unique=True)
    region = models.CharField(max_length=30)
    countries = models.TextField(default="")

    def __str__(self):
        return self.region
