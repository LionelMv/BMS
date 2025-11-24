from django.db import models
from django.db import transaction
from django.utils import timezone
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
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    @transaction.atomic
    def save(self, *args, **kwargs):
        # On create, decrement stock atomically
        is_create = self.pk is None
        if is_create:
            prod = Product.objects.select_for_update().get(pk=self.product_id)
            if prod.quantity < self.quantity:
                raise ValueError("Insufficient stock")
            prod.quantity -= self.quantity
            prod.save()
            # create stock history

            StockHistory.objects.create(product=prod, change=-self.quantity, reason=f"Sale #{self.pk or 'new'}")
        super().save(*args, **kwargs)
