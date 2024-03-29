from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework.exceptions import NotAcceptable
from students.models import Student
from utils.get_object_or_404 import get_object_or_404

from courses.models import Course


class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_teacher


class IsOwnerAndAdminToDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "DELETE":
            return request.user.is_superuser

        return request.user == obj.owner


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.owner


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_teacher


class StudentHaventCourse(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return False

        course_id = view.kwargs.get("course_id")
        course = get_object_or_404(Course, pk=course_id)
        try:
            Student.objects.get(course=course, student=request.user)
            raise NotAcceptable(detail="You have already purchased this course")
        except ObjectDoesNotExist:
            return True
