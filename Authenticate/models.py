from django.db import models
from django.contrib.auth.models import User

# Extend the default User model with extra fields
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    fullname = models.CharField(max_length=100, blank=True)
    cooldown = models.IntegerField(default=3)
    verified = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

# Create your models here.
