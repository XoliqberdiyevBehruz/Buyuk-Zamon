from django.dispatch import receiver
from django.db.models.signals import post_save

from account import models 


@receiver(post_save, sender=models.Payment)
def change_student_info(sender, instance, **kwargs): 


    user = instance.user
    user.paid = (user.paid if user.paid else 0) + int(instance.price)
    if user.debt > user.paid:
        user.debt = user.debt - user.paid
        if user.debt < 0:
            user.debt = 0
            user.save()
    if user.debt == 0:
        user.is_debt = False
    user.save()

