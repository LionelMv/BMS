from rest_framework import viewsets, permissions
from apps.inventory.models import Product
from apps.inventory.serializers import ProductSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-updated_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def low_stock(self, request: Request) -> Response:
        qs = self.get_queryset().filter(quantity__lte=models.F('low_stock_threshold'))
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
