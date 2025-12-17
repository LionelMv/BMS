from __future__ import annotations
from typing import Any, Dict, TYPE_CHECKING
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import Employee


if TYPE_CHECKING:
    from apps.core.models import User as UserType

User = get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "is_active", "salary", "total_leave_days", "leave_taken", "role_note"]

class UserSerializer(serializers.ModelSerializer):
    employee_profile = EmployeeSerializer(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    roles = serializers.CharField(write_only=True, required=False, help_text="Comma-separated group names")
    role_list = [r.strip() for r in roles.split(",")] if roles else []
    assigned_roles = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password", "is_active", "employee_profile", "roles", "assigned_roles"]
        read_only_fields = ["id", "employee_profile", "assigned_roles"]

    def get_assigned_roles(self, obj: UserType) -> list[str]:
        return [group.name for group in obj.groups.all()]

    def create(self, validated_data: Dict[str, Any]) -> UserType:
        roles = validated_data.pop("roles", [])
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        # ensure Employee profile exists
        Employee.objects.get_or_create(user=user)
        # attach roles
        if roles:
            groups = Group.objects.filter(name__in=roles)
            user.groups.set(groups)
        return user

    def update(self, instance: UserType, validated_data: Dict[str, Any]) -> UserType:
        roles = validated_data.pop("roles", None)
        password = validated_data.pop("password", None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        if password:
            instance.set_password(password)
        instance.save()
        if roles is not None:
            groups = Group.objects.filter(name__in=roles)
            instance.groups.set(groups)
        return instance
