from django.db import models

from account.models import BaseModel


class ExpenceCategory(BaseModel):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class Expence(BaseModel):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(ExpenceCategory, on_delete=models.SET_NULL, null=True, related_name='expence_category')
    date = models.DateField()
    price = models.PositiveBigIntegerField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name