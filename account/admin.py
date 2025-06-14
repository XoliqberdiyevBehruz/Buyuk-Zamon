from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as Admin 
from django.contrib.auth.models import Group

from account import models 

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','full_name', 'phone_number', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    ordering = ('id',)

@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'position', 'is_staff')
    list_filter = ('is_staff', 'is_active')


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(models.EmployeeSalary)
class EmployeeSalary(admin.ModelAdmin): 
    list_display = ('id', 'employee', 'salary', 'date')
    ordering = ('id',)
    search_fields = ('employee__full_name',)
    list_filter = ('employee__full_name',)