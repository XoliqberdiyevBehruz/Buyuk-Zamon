from django.db import models
from django.contrib.auth.models import AbstractUser

PREMIUM, VIP, BUSINESS = ('premium', 'vip', 'biznes')
CASH, CREDIT, CARD = ('naqd', 'nasya', 'karta')

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
    TARIFF = (
        (PREMIUM, PREMIUM),
        (VIP, VIP),
        (BUSINESS, BUSINESS),
    )
    PAYMENT_TYPE = (
        (CASH, CASH), 
        (CREDIT, CREDIT),
        (CARD, CARD),
    )
    full_name = models.CharField(max_length=250, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
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
    tariff = models.CharField(max_length=50, choices=TARIFF)
    payment_type = models.CharField(max_length=15, choices=PAYMENT_TYPE)
    group_joined = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    
    class Meta:
        unique_together = ('phone_number', 'full_name', 'card_number')
    

class Payment(BaseModel):
    PAYMENT_TYPE = (
        ('cash', 'cash'),
        ('card', 'card'),
        ('credit', 'credit'),
    )
    BANK = (
        ('uzum', 'uzum'),
        ('alif', 'alif'),
        ('anor', 'anor'),
        ('zoodpay', 'zoodpay'),
        ('click', 'click'),
        ('payme', 'payme'),
    )
    user = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    payment_time = models.CharField(max_length=200, null=True, blank=True)
    price = models.PositiveBigIntegerField(null=True, blank=True)
    payment_id = models.CharField(max_length=250, null=True, blank=True)
    type = models.CharField(max_length=50, choices=PAYMENT_TYPE, default='cash')
    bank = models.CharField(max_length=50, choices=BANK, null=True, blank=True)

    def __str__(self):
        return str(self.price)
    
    def save(self, *args, **kwargs):
        if self.type == 'naqd':
            self.bank = None
        super().save(*args, **kwargs)