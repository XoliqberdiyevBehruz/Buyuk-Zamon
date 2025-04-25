from django.contrib import admin

from course import models 
# Register your models here.


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']


@admin.register(models.Payment)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'course', 'paid', 'debt', 'is_debt']
