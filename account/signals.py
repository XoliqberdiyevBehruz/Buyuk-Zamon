from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from account import models 


@receiver(post_save, sender=models.Payment)
def change_student_info(sender, instance, **kwargs): 
    user = instance.user
    user.paid = (user.paid if user.paid else 0) + instance.price

    user.debt = user.course_price - user.paid
    if user.debt == 0 or user.debt < 0:
        user.is_debt = False
        user.debt = 0
    user.save()


@receiver(post_delete, sender=models.Payment)
def remove_payment_from_student(sender, instance, **kwargs):
    if instance.user:
        user = instance.user
        user.paid -= instance.price
        user.debt += instance.price
        if user.debt < 0:
            user.is_debt = True
        user.save()