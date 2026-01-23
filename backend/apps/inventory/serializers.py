from decimal import Decimal

from rest_framework import serializers

from apps.inventory.models import Product, Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "quantity",
            "price",
            "low_stock_threshold",
            "supplier",
            "created_at",
            "updated_at",
        ]

    def validate_price(self, value: Decimal) -> Decimal:
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value

    def validate_low_stock_threshold(self, value: Decimal) -> Decimal:
        if value < 0:
            raise serializers.ValidationError("Threshold cannot be negative")
        return value
