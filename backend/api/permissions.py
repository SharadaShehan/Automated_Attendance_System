from rest_framework import permissions
from database.models import CustomUser


class ViewAnyEmployeePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role.is_manager or request.user.role.is_executive :
            if request.user.company.id == obj.company.id:
                return True
        return False


class ViewOwnAccountPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.id:
            return True
        return False


class EditAnyEmployeePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role.is_executive:
            return True
        return False


class ViewAllEmployeesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role.is_manager or request.user.role.is_executive:
            return True
        return False


class ViewAnyRolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role.is_executive:
            return True
        return False


class ViewAllRolesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role.is_executive :
            return True
        return False


class DeleteAnyRolePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role.is_executive :
            if request.user.company.id == obj.company.id:
                if obj.default_key == request.user.company.default_role_key:
                    return False
                query_set = CustomUser.objects.filter(role=obj)
                if not query_set.exists():
                    return True
        return False

