from rest_framework import generics
from apps.sales.models import Sale
from apps.sales.serializers import SaleSerializer


class SaleCreateView(generics.CreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


class SaleListView(generics.ListAPIView):
    queryset = Sale.objects.select_related("product", "customer", "employee")
    serializer_class = SaleSerializer
