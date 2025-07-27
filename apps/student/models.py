from datetime import datetime, time

from django.db import models
from django.utils.timezone import make_aware

from apps.account.models import BaseModel 

PREMIUM, VIP, BUSINESS = ('premium', 'vip', 'biznes')
CASH, CREDIT, CARD = ('naqd', 'nasya', 'karta')


class TelegramGroup(BaseModel):
    name = models.CharField(max_length=250)
    group_id = models.BigIntegerField(unique=True)
    students = models.ManyToManyField('Student', related_name='telegram_groups')
    type = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} ---- {self.group_id}"


class Student(BaseModel):
    TARIFF = (
        (PREMIUM, PREMIUM),
        (VIP, VIP),
        (BUSINESS, BUSINESS),
    )
    STUDENT_STATUS = (
        ('prepayment', 'prepayment'),
        ('partially', 'partially'),
        ('completed', 'completed'),
    )

    MONTH = (
        ('yanvar', 'yanvar'),
        ('fevral', 'fevral'),
        ('mart', 'mart'),
        ('aprel', 'aprel'),
        ('may', 'may'),
        ('iyun', 'iyun'),
        ('iyul', 'iyul'),
        ('avgust', 'avgust'),
        ('sentabr', 'sentabr'),
        ('oktabr', 'oktabr'),
        ('noyabr', 'noyabr'),
        ('dekabr', 'dekabr')
    )
    STUDENT_TYPE = (
        ('new', 'new'),
        ('study', 'study'),
        ('graduate', 'graduate'),
    )
    STUDY_TYPE = (
        ('offline', 'offline'),
        ('online', 'online'),
    )

    full_name = models.CharField(max_length=250, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    student_id_time = models.DateField(null=True, blank=True)
    student_id = models.PositiveBigIntegerField(null=True, blank=True)

    contract_number = models.CharField(max_length=250, null=True, blank=True)
    course_price = models.PositiveBigIntegerField(default=0)
    paid = models.IntegerField(null=True, blank=True)
    debt = models.IntegerField(null=True, blank=True)
    is_debt = models.BooleanField(default=True)
    
    tariff = models.CharField(max_length=50, choices=TARIFF)
    status = models.CharField(max_length=25, choices=STUDENT_STATUS)
    type = models.CharField(max_length=20, choices=STUDENT_TYPE, default='new')
    study_type = models.CharField(max_length=10, choices=STUDY_TYPE, default='offline')

    is_blacklist = models.BooleanField(default=False)
    group_joined = models.BooleanField(default=False)
    suprice = models.BooleanField(default=False)
    month = models.CharField(choices=MONTH, max_length=50, default='aprel')

    employee = models.ForeignKey(
        'account.Employee', on_delete=models.SET_NULL, null=True,related_name='students'
    )
    coach = models.ForeignKey(
        'account.Employee', on_delete=models.CASCADE, null=True, related_name='coach_students'
    )

    telegram_id = models.CharField(max_length=250, null=True, blank=True)
    telegram_full_name = models.CharField(max_length=250, null=True, blank=True)
    telegram_username = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if self.paid:
            if self.paid < 3_000_000:
                self.status = 'prepayment'
                self.is_debt = True
            elif self.paid > 3_000_000 and self.paid < self.course_price:
                self.status = 'partially'
                self.is_debt = True
            elif self.paid >= self.course_price:
                self.status = 'completed'
                self.is_debt = False
        return super().save(*args, **kwargs)


class Payment(BaseModel):
    PAYMENT_TYPE = (
        ('cash', 'cash'),
        ('card', 'card'),
        ('credit', 'credit'),
    )
    BANK = (
        ("cash_uzs", 'cash_uzs'),
        ("cash_usd", "cash_usd"),
        ("account_number", "account_number"),
        ('alif', 'alif'),
        ('anor', 'anor'),
        ('uzum', 'uzum'),
        ("P2P", "P2P"),
        ("other", "other"),
        ("payme", "payme"),
        ("click", "click"),
    )

    user = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    payment_time = models.DateField(null=True)
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


class PaymentImage(BaseModel):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='account/payment/%Y/%m/')

    def __str__(self):
        return str(self.image)


class Notification(BaseModel):
    full_name = models.CharField(max_length=250, null=True)
    phone_number = models.CharField(max_length=250, null=True)
    contract_number = models.CharField(max_length=250, null=True)
    description = models.TextField()

    def __str__(self):
        return self.full_name or self.description


class StudentGroup(BaseModel):
    start_date = models.DateField()
    end_date = models.DateField()
    group_name = models.CharField(max_length=250)
    start_date_online = models.DateField()
    start_date_offline = models.DateField()
    students = models.ManyToManyField(Student, related_name="groups")

    def __str__(self):
        return self.group_name
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            start_datetime = make_aware(datetime.combine(self.start_date, time.min))
            end_datetime = make_aware(datetime.combine(self.end_date, time.max))
            students_to_add = Student.objects.filter(student_id_time__range=(start_datetime, end_datetime))
            self.students.add(*students_to_add)
    

class StudentMessage(BaseModel):
    message = models.CharField(max_length=500)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f'{self.student} - {self.message}'
    