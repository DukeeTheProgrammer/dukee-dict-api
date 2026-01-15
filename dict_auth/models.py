from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_enabled = models.BooleanField(default=False)
    token = models.CharField(max_length=200, blank=True)
    api_key = models.CharField(max_length=300, blank=True)
    logged_in = models.BooleanField(default=False)


