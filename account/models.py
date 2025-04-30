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
    full_name = models.CharField(max_length=250, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    total_price = models.PositiveBigIntegerField(default=0)
    profile_photo = models.ImageField(upload_to='account/student/profile_photo/%Y/%m/', null=True, blank=True)
    card_number = models.CharField(max_length=16, null=True, blank=True)
    group_id = models.CharField(max_length=250, null=True, blank=True)
    telegram_link = models.CharField(max_length=200, null=True, blank=True)
    contract_number = models.CharField(max_length=250, null=True, blank=True)
    course_price = models.PositiveBigIntegerField(default=10000000)
    paid = models.IntegerField(null=True, blank=True)
    debt = models.IntegerField(null=True, blank=True)
    is_debt = models.BooleanField(default=False)
    def __str__(self):
        return self.full_name
    
    class Meta:
        unique_together = ('phone_number', 'full_name', 'card_number')
    

class Payment(BaseModel):
    PAYMENT_TYPE = (
        ('naxt', 'naxt'),
        ('click', 'click'),
        ('alif_bank', 'alif_bank'),
        ('uzum_bank', 'uzum_bank'),
        ('hisob_raqam', 'hisob_raqam'),
        ('zoodpay', 'zoodpay'),
        ('visa', 'visa'),
        ('anor_bank', 'anor_bank'),
    )
    user = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    payment_time = models.CharField(max_length=200, null=True, blank=True)
    price = models.PositiveBigIntegerField(null=True, blank=True)
    payment_id = models.CharField(max_length=250, null=True, blank=True)
    type = models.CharField(max_length=250, choices=PAYMENT_TYPE, default='naxt')

    def __str__(self):
        return str(self.price)