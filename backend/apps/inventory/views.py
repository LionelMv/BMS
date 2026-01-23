from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.inventory.models import Product, Supplier
from apps.inventory.serializers import ProductSerializer, SupplierSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("supplier").order_by("-updated_at")
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"])
    def low_stock(self, request: Request) -> Response:
        qs = self.get_queryset().filter(quantity__lte=models.F("low_stock_threshold"))
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
