from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 


class User(BaseModel, AbstractUser):
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.phone_number
