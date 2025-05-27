from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver    

from account.models import Employee, EmployeeSalary
from finance.models import Expence, ExpenceCategory


@receiver(post_save, sender=EmployeeSalary)
def create_expence(sender, instance, created, **kwargs):
    if created:
        Expence.objects.create(
                name=instance.employee.full_name,
                category=ExpenceCategory.objects.get_or_create(name='Hodim oyligi')[0],
                date=instance.date,
                price=instance.salary,
                description=f'{instance.employee.full_name} oylik berildi' 
            )   