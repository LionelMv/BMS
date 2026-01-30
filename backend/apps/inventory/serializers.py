from decimal import Decimal
from typing import Any

from rest_framework import serializers

from apps.inventory.models import Product, StockHistory, Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.only("id", "name"),
        source="supplier",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "quantity",
            "price",
            "low_stock_threshold",
            "supplier",
            "supplier_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    # ---- Shared Positive Validator ----
    def _validate_positive(self, value: Any, field_name: str):
        if value < 0:
            message = f"{field_name} cannot be negative"
            raise serializers.ValidationError(message)
        return value

    def validate_price(self, value: Decimal) -> Decimal:
        return self._validate_positive(value, "Price")

    def validate_low_stock_threshold(self, value: int) -> int:
        return self._validate_positive(value, "Low stock threshold")


class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name"]


class StockHistorySerializer(serializers.ModelSerializer):
    product = ProductMiniSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.only("id", "name"),
        source="product",
        write_only=True,
    )

    performed_by = serializers.StringRelatedField(read_only=True)  # type: ignore[var-annotated]

    class Meta:
        model = StockHistory
        fields = [
            "id",
            "product",
            "product_id",
            "change",
            "reason",
            "performed_by",
            "created_at",
        ]
        read_only_fields = ["created_at"]
