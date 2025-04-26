from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as Admin 
from django.contrib.auth.models import Group

from account import models 


admin.site.register(models.Student)
admin.site.register(models.Payment)