from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from apps.core.models import Employee
from .serializers import EmployeeSerializer
from .permissions import IsAdminOrManager

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related("employee_profile").all().order_by("-id")
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=["get", "put"], permission_classes=[IsAdminOrManager])
    def employee(self, request: Request, pk: int) -> Response:
        user = self.get_object()
        employee, _ = Employee.objects.get_or_create(user=user)

        if request.method == "GET":
            serializer = EmployeeSerializer(employee)

        elif request.method == "PUT":
            serializer = EmployeeSerializer(employee, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data)
