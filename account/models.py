from django.db import models
from django.contrib.auth.models import AbstractUser

from account.managers import CustomUserManager

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(BaseModel, AbstractUser):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    username = None
    first_name = None
    last_name = None
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.phone_number
    

class Employee(User):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='employees')
    salary = models.PositiveBigIntegerField(default=0)
    date_of_joined = models.DateField(null=True, blank=True)
    paid = models.PositiveBigIntegerField(default=0)
    indebtedness = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.full_name
    

class EmployeeSalary(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salaries')
    salary = models.PositiveBigIntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.full_name} - {self.salary}"