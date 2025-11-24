from django.db import models
from django.db import transaction
from django.utils import timezone
from typing import Any
from apps.inventory.models import Product, StockHistory
from apps.core.models import Employee

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    @classmethod
    @transaction.atomic
    def create_sale(
        cls,
        *,
        product: Product,
        customer: Customer | None,
        employee: Employee,
        quantity: int,
        total_price: float,
    ) -> "Sale":

        prod = Product.objects.select_for_update().get(pk=product.pk)

        if prod.quantity < quantity:
            raise ValueError("Insufficient stock")

        prod.quantity -= quantity
        prod.save()

        sale = cls(
            product=product,
            customer=customer,
            employee=employee,
            quantity=quantity,
            total_price=total_price,
        )
        sale.save()

        StockHistory.objects.create(
            product=prod,
            change=-quantity,
            reason=f"Sale #{sale.pk}",
        )

        return sale
    
    def save(self, *args: Any, **kwargs: Any) -> None:
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['employee']),
        ]
