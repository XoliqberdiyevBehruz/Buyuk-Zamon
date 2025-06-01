from django.contrib import admin

from student import models


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'is_debt', 'paid', 'debt', 'course_price', 'tariff']


class PaymentImageInline(admin.TabularInline):
    model = models.PaymentImage
    extra = 0


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'payment_time', 'type']
    inlines = [PaymentImageInline]


@admin.register(models.StudentDescription)
class StudentDescriptionAdmin(admin.ModelAdmin):
    pass