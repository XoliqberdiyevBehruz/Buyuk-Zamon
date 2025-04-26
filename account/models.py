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
    full_name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=15, unique=True)
    total_price = models.CharField(max_length=250, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='account/student/profile_photo/%Y/%m/', null=True, blank=True)
    card_number = models.CharField(max_length=16)
    group_id = models.CharField(max_length=250)
    telegram_link = models.CharField(max_length=200, null=True, blank=True)
    contract_number = models.CharField(max_length=250, null=True, blank=True)
    course_price = models.CharField(max_length=250, null=True, blank=True)
    paid = models.CharField(max_length=250, null=True, blank=True)
    debt = models.CharField(max_length=250, null=True, blank=True)
    is_debt = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    

class Payment(BaseModel):
    user = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='payments')
    payment_time = models.CharField(max_length=200)
    price = models.CharField(max_length=250)
    payment_id = models.CharField(max_length=250)

    def __str__(self):
        return self.price 

