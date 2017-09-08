from django.db import models

class UserInfo(models.Model):
    username = models.CharField(max_length=32,verbose_name='用户名')
    email = models.EmailField(verbose_name='邮箱')

class Role(models.Model):
    name = models.CharField(max_length=32,verbose_name='角色')
