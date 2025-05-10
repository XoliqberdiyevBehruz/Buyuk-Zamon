from django.db import models
from django.contrib.auth.models import AbstractUser

from account.managers import CustomUserManager

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(BaseModel, AbstractUser):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    username = None
    first_name = None
    last_name = None
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.phone_number
    



class Employee(User):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='employees')

    def __str__(self):
        return self.full_name
    