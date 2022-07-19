from courses.models import Course
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework.exceptions import NotAcceptable
from students.models import Student
from utils import get_object_or_404


class IsReviewOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True

        return obj.user == request.user


class StudentHaveCourse(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        course_id = view.kwargs.get("course_id")
        course = get_object_or_404(Course, detail="Course not found", pk=course_id)
        try:
            Student.objects.get(course=course, student=request.user)
            return True
        except ObjectDoesNotExist:
            raise NotAcceptable(detail="You haven't purchased this course")
