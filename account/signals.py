from django.dispatch import receiver
from django.db.models.signals import post_save

from account import models 


@receiver(post_save, sender=models.Payment)
def change_student_info(sender, **kwargs): 
    user = sender.user
    user.paid = int(sender.price)
    user.debt = user.debt - user.price
    if user.debt == 0:
        user.is_debt = False
    user.save()

