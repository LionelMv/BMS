from __future__ import annotations
from typing import Any
from rest_framework.permissions import BasePermission, SAFE_METHODS


# ---------------------------------------------------------
# Base role-checking utility
# ---------------------------------------------------------

def user_in_groups(user, groups: list[str]) -> bool:
    """Return True if user belongs to ANY of the given groups."""
    return user.groups.filter(name__in=groups).exists()


# ---------------------------------------------------------
# INDIVIDUAL ROLE PERMISSIONS
# ---------------------------------------------------------

class IsAdmin(BasePermission):
    """Allow access only to Admin (or superuser)."""

    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated and
            (request.user.is_superuser or user_in_groups(request.user, ["Admin"]))
        )


class IsManager(BasePermission):
    """Allow access only to Manager role."""

    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated and
            user_in_groups(request.user, ["Manager"])
        )


class IsSupervisor(BasePermission):
    """Allow access only to Supervisor role."""

    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated and
            user_in_groups(request.user, ["Supervisor"])
        )


class IsEmployee(BasePermission):
    """Allow access only to Employee role."""

    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated and
            user_in_groups(request.user, ["Employee"])
        )


# ---------------------------------------------------------
# HIERARCHY PERMISSIONS
# ---------------------------------------------------------

class IsAdminOrManager(BasePermission):
    """Admin or Manager can access."""

    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated and
            (
                request.user.is_superuser or
                user_in_groups(request.user, ["Admin", "Manager"])
            )
        )


class IsSupervisorOrHigher(BasePermission):
    """Supervisor, Manager, or Admin can access."""

    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated and
            (
                request.user.is_superuser or
                user_in_groups(request.user, ["Admin", "Manager", "Supervisor"])
            )
        )


class IsEmployeeOrHigher(BasePermission):
    """
    Allows Employee, Supervisor, Manager, Admin.

    Useful for actions accessible to ALL roles except anon.
    """

    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated


# ---------------------------------------------------------
# SELF-MODIFICATION RULES
# ---------------------------------------------------------

class IsEmployeeSelf(BasePermission):
    """
    Employee can modify ONLY their own profile.
    Works with Employee model where obj.user == request.user.
    """

    def has_object_permission(self, request, view, obj: Any) -> bool:
        return (
            request.user.is_authenticated and
            hasattr(obj, "user") and
            obj.user == request.user
        )


# ---------------------------------------------------------
# REPORT ACCESS RULES
# ---------------------------------------------------------

class CanViewFullReports(BasePermission):
    """Admin and Manager access full reports."""

    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated and (
                request.user.is_superuser or
                user_in_groups(request.user, ["Admin", "Manager"])
            )
        )


class CanViewLimitedReports(BasePermission):
    """Employees & Supervisors can see limited reports."""

    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated and
            user_in_groups(request.user, ["Employee", "Supervisor"])
        )


# ---------------------------------------------------------
# GENERIC SAFE READ PERMISSION
# ---------------------------------------------------------

class ReadOnly(BasePermission):
    """Allow all authenticated users to read, deny modifications."""

    def has_permission(self, request, view) -> bool:
        return (
            request.method in SAFE_METHODS
        )
