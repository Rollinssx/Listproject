import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from ListProject import settings

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(null=False, max_length=200)
    last_name = models.CharField(null=False, max_length=200)
    username = models.CharField(null=False, max_length=200, unique=True)
    password = models.CharField(null=False, max_length=200)
    email = models.EmailField(null=False, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class ToDoList(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    list_name = models.CharField(null=False, default='My List', max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='todolists', null=True)

    def __str__(self):
        return self.list_name


class ToDoItem(models.Model):
    list = models.ForeignKey(ToDoList, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description



