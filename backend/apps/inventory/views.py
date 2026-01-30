from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.inventory.models import Product, StockHistory, Supplier
from apps.inventory.serializers import (
    ProductSerializer,
    StockHistorySerializer,
    SupplierSerializer,
)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.select_related("supplier").order_by("-updated_at")

    @action(detail=False, methods=["get"])
    def low_stock(self, _request: Request) -> Response:
        qs = self.get_queryset().low_stock()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def out_of_stock(self, _request: Request) -> Response:
        qs = self.get_queryset().out_of_stock()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class StockHistoryViewSet(viewsets.ModelViewSet):
    queryset = StockHistory.objects.select_related("product", "performed_by")
    serializer_class = StockHistorySerializer
