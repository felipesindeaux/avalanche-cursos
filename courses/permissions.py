from rest_framework import permissions
from courses.models import Course
from students.models import Student

from django.core.exceptions import ObjectDoesNotExist
from utils.get_object_or_404 import get_object_or_404


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


class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_teacher


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
        course_id = view.kwargs.get("course_id")
        course = get_object_or_404(Course, pk=course_id)
        try:
            Student.objects.get(course=course, student=request.user)
        except ObjectDoesNotExist:
            return True
