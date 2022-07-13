# from courses.models import Course
from courses.models import Course
from django.shortcuts import get_object_or_404
from rest_framework.permissions import SAFE_METHODS, BasePermission

from lessons.models import Lesson


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        course_id = view.kwargs.get("course_id")

        course = get_object_or_404(Course, pk=course_id)

        return course.owner.id == request.user.id


class IsStudentRetrieve(BasePermission):
    def has_permission(self, request, view):
        return False


class IsOwnerUpdate(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("PATCH", "PUT"):
            course_id = view.kwargs.get("course_id")
            lesson_id = view.kwargs.get("pk")

            course = get_object_or_404(Course, pk=course_id)

            lesson = get_object_or_404(Lesson, pk=lesson_id)

            is_owner = course.owner.id == request.user.id

            is_lesson_in_course = str(lesson.course.id) == str(course_id)

            return is_owner and is_lesson_in_course

        return False


class IsAdminDelete(BasePermission):
    def has_permission(self, request, view):
        return request.method == "DELETE" and request.user.is_superuser
