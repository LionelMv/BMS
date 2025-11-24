from django.db import models
from django.utils import timezone

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    low_stock_threshold = models.IntegerField(default=5)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

class StockHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='history')
    change = models.IntegerField()  # positive for addition, negative for removal
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
