from django.db import models

class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField()

class Role(models.Model):
    name = models.CharField(max_length=32)
