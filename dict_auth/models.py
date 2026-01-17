from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    api_enabled = models.BooleanField(default=False)
    token = models.CharField(max_length=200, blank=True)
    api_key = models.CharField(max_length=300, blank=True)
    logged_in = models.BooleanField(default=False)
    def __str__(self):
        return str(self.user.first_name)

class Log(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, related_name="logs")
    requests = models.IntegerField(default=0, blank=True, null=True)
    ip = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return str(self.profile.user.first_name)
