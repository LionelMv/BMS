from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.conf import settings
from django.db import models

class User(AbstractUser):
    # You can add fields if needed, e.g. phone, department, etc.
    # But for now, just use the default fields + username/email.
    # Optional: add audit fields, etc.
    pass


class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )
    # Employee-specific fields
    is_active = models.BooleanField(default=True)
    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
        )
    total_leave_days = models.IntegerField(default=0)
    leave_taken = models.IntegerField(default=0)
    # Other fields as needed, e.g. department, title
    role_note = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        indexes = [
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.user.username} (Employee)"
