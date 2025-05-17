from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver    

from account.models import Employee, EmployeeSalary
from finance.models import Expence, ExpenceCategory


@receiver(post_save, sender=EmployeeSalary)
def update_employee_paid_indebtedness(sender, instance, created, **kwargs):
    instance.employee.paid += instance.salary
    instance.employee.indebtedness = instance.employee.salary - instance.employee.paid
    instance.employee.save()

@receiver(pre_delete, sender=EmployeeSalary)
def update_employee_paid_indebtedness_on_delete(sender, instance, **kwargs):
    instance.employee.paid -= instance.salary
    instance.employee.indebtedness = instance.employee.salary - instance.employee.paid
    instance.employee.save()

@receiver(post_save, sender=EmployeeSalary)
def create_expence(sender, instance, created, **kwargs):
    if created:
        Expence.objects.create(
                name=instance.employee.full_name,
                category=ExpenceCategory.objects.get_or_create(name='oylik maosh')[0],
                date=instance.date,
                price=instance.salary,
                description=f'{instance.employee.full_name} oylik berildi' 
            )   
     
