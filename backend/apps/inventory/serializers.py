from rest_framework import serializers
from apps.inventory.models import Product, Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Supplier.objects.all(), source='supplier', required=False)

    class Meta:
        model = Product
        fields = ['id','name','quantity','price','low_stock_threshold','supplier','supplier_id','created_at','updated_at']
