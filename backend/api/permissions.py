from rest_framework import permissions
from database.models import CustomUser, Company


class ViewAnyEmployeePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role.has_read_permission or request.user.role.has_edit_permission:
            return True
        return False


class ViewOwnAccountPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.id:
            return True
        return False


class EditAnyEmployeePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role.has_edit_permission:
            return True
        return False


class ViewAllEmployeesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role.has_read_permission or request.user.role.has_edit_permission:
            return True
        return False


class ViewAnyRolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role.has_edit_permission:
            return True
        return False


class ViewAllRolesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role.has_edit_permission:
            return True
        return False


class DeleteAnyRolePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role.has_edit_permission:
            if obj.id == Company.objects.get_company().default_role.id:
                return False
            query_set = CustomUser.objects.filter(role=obj)
            if not query_set.exists():
                return True
        return False
