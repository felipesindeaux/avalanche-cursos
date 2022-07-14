from courses.models import Course
from django.shortcuts import get_object_or_404
from rest_framework.permissions import SAFE_METHODS, BasePermission

from lessons.models import Lesson


class OwnerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "DELETE":
            return False

        course_id = view.kwargs.get("course_id")

        course = get_object_or_404(Course, pk=course_id)

        self.course = course

        return course.owner.id == request.user.id

    def has_object_permission(self, request, view, obj):

        lesson_id = view.kwargs.get("pk")

        lesson = get_object_or_404(Lesson, pk=lesson_id)

        is_owner = self.course.owner.id == request.user.id

        is_lesson_in_course = str(lesson.course_id) == str(self.course.id)

        return is_owner and is_lesson_in_course


class StudentOrAdminReadOnly(BasePermission):
    def has_permission(self, request, view):
        course_id = view.kwargs.get("course_id")

        course = get_object_or_404(Course, pk=course_id)

        if request.method in SAFE_METHODS:
            return request.user.is_superuser
            # or request.user in course.students

        return False


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method == "DELETE" and request.user.is_superuser
