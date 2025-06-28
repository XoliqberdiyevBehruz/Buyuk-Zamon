from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as Admin 
from django.utils.translation import gettext_lazy as _

from account import models 

@admin.register(models.User)
class UserAdmin(Admin):
    list_display = ('id','full_name', 'phone_number', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    ordering = ('id',)

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ("full_name", "email", 'role', '')}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "password1", "password2"),
            },
        ),
    )

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