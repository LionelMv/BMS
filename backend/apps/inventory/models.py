from typing import Self

from django.conf import settings
from django.db import models
from django.db.models import F


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class ProductQuerySet(models.QuerySet["Product"]):
    def low_stock(self) -> Self:
        return self.filter(quantity__lte=F("low_stock_threshold"))

    def out_of_stock(self) -> Self:
        return self.filter(quantity__lte=0)


class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    low_stock_threshold = models.IntegerField(default=5)
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return self.name


class StockHistory(models.Model):
    class ReasonChoices(models.TextChoices):
        ADJUSTMENT = "ADJUSTMENT", "Adjustment"
        SALE = "SALE", "Sale"
        PURCHASE = "PURCHASE", "Purchase"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="history",
    )
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    change = models.IntegerField()  # positive for addition, negative for removal
    reason = models.CharField(max_length=50, choices=ReasonChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["product", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.product.name}: {self.change}"
