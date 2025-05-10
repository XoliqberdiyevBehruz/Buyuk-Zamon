from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as Admin 
from django.contrib.auth.models import Group

from account import models 

@admin.register(models.User)
class UserAdmin(Admin):
    list_display = ('id','full_name', 'phone_number', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    ordering = ('id',)

@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'position', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal info", {"fields": ("full_name", "position")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)
    search_fields = ('name',)
    list_filter = ('name',)