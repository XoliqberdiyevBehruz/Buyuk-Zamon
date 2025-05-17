from django.contrib import admin

from finance import models


@admin.register(models.Expence)
class ExpenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price')


@admin.register(models.ExpenceCategory)
class ExpenceCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')