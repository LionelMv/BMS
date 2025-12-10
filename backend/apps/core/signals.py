from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from .models import User, Employee
from django.contrib.auth.models import Group


@receiver(post_save, sender=User)
def create_employee_profile(sender, instance: User, created: bool, **kwargs) -> None:
    if created:
        Employee.objects.create(user=instance)

    else:
        # ensure profile exists for existing user
        Employee.objects.get_or_create(user=instance)

@receiver(post_migrate)
def create_default_groups(sender, **kwargs) -> None:
    """
    Create default groups/roles AFTER migrations.
    """
    if sender.name != "apps.core":
        return

    for name in ("Admin", "Manager", "Employee"):
        Group.objects.get_or_create(name=name)