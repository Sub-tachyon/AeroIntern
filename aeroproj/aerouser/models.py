from django.db import models
from django.db import models
from django.utils import timezone
import uuid


class userdata(models.Model):
    username=models.CharField(max_length=255,null=True)
    email = models.CharField(max_length=255,null=True)
    password = models.CharField(max_length=255,null=True)
    

class PasswordResetToken(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100, editable=False) 
    

    def __str__(self):
        return f"Password Reset Token for {self.email}"
