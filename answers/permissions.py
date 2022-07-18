from django.shortcuts import get_object_or_404
from rest_framework import permissions

from answers.models import Answer


class IsOwnerAndAdminToDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        answer_id = view.kwargs.get("answer_id")
        answer = get_object_or_404(Answer, pk=answer_id)

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "DELETE":
            if request.user.is_superuser:
                return True
            return request.user.id == answer.user_id

        return request.user.id == answer.user_id
