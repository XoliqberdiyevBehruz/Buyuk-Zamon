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


class Student(BaseModel):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    father_name = models.CharField(max_length=25, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    passport_series = models.CharField(max_length=10, null=True, blank=True, unique=True)
    birth_place = models.CharField(max_length=50, null=True, blank=True)
    live_address = models.CharField(max_length=50, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='account/student/profile_photo/%Y/%m/', null=True, blank=True)

    def __str__(self):
        return self.first_name + self.last_name
    



