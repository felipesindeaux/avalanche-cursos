from rest_framework import permissions


class IsAdminToDelete(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method != "DELETE":
            return True

        return request.user.is_superuser


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True

        return request.user.is_teacher


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        return request.user == obj.owner