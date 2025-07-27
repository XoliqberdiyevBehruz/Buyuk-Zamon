from django.contrib import admin

from apps.student import models


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


@admin.register(models.Notification)
class StudentDescriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TelegramGroup)
class TelegramGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(models.StudentMessage)
class StudentMessageAdmin(admin.ModelAdmin):
    pass