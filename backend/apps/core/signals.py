from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Employee


@receiver(post_save, sender=User)
def create_employee_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)
