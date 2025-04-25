from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as Admin 
from django.contrib.auth.models import Group

from account import models 
# Register your models here

@admin.register(models.User)
class UserAdmin(Admin):
    pass 

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name']










# unregister Group from django admin panel
admin.site.unregister(Group)