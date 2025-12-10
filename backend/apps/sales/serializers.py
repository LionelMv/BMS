from rest_framework import serializers
from apps.sales.models import Sale, Customer
from apps.inventory.models import Product
from apps.core.models import Employee


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "email", "phone"]


class SaleSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product"
    )
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source="customer",
        allow_null=True,
        required=False,
    )
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source="employee"
    )

    class Meta:
        model = Sale
        fields = [
            "id",
            "product_id",
            "customer_id",
            "employee_id",
            "quantity",
            "total_price",
            "date",
        ]
        read_only_fields = ["id", "date"]

    def create(self, validated_data: dict) -> "Sale":
        """Create a sale."""
        try:
            sale = Sale.create_sale(**validated_data)
        except ValueError as e:
            # Convert to DRF validation error
            raise serializers.ValidationError({"detail": str(e)})

        return sale
