from django.shortcuts import get_object_or_404
from rest_framework import permissions

from questions.models import Question
from users.models import User


class IsOwnerAndAdminToDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        question_id = view.kwargs.get("question_id")
        question = get_object_or_404(Question, pk=question_id)

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "DELETE":
            if request.user.is_superuser:
                return True
            return request.user.id == question.user_id

        return request.user.id == question.user_id
