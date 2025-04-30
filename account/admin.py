from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as Admin 
from django.contrib.auth.models import Group

from account import models 


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'is_debt', 'paid', 'debt', 'course_price', 'payment_type', 'tariff']


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'payment_time', 'type']