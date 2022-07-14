from courses.models import Course
from rest_framework.permissions import SAFE_METHODS, BasePermission
from students.models import Student
from utils.get_object_or_404 import get_object_or_404

# Permissão de Owner   (read, create, update)
# Permissão de Admin   (read, delete)
# Permissão de Student (read)


class OwnerAdminStudentReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            if request.user.is_superuser:
                return True

            course_id = view.kwargs.get("course_id")
            course = get_object_or_404(Course, "Course not found", pk=course_id)

            is_owner = course.owner == request.user

            if is_owner:
                return True

            is_student = get_object_or_404(
                Student,
                "You must an admin, owner or student from this course",
                course=course_id,
                student=request.user.id,
            )

            return bool(is_student)

        return False

    def has_object_permission(self, request, view, obj):
        return str(obj.course_id) == view.kwargs.get("course_id")


class OwnerCreateUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("POST", "PATCH", "PUT"):
            course_id = view.kwargs.get("course_id")

            course = get_object_or_404(
                Course,
                "You must be the owner of the course to perform this action",
                pk=course_id,
            )

            return course.owner == request.user

        return False

    def has_object_permission(self, request, view, obj):
        return str(obj.course_id) == view.kwargs.get("course_id")


class AdminDeletePermission(BasePermission):
    def has_permission(self, request, view):
        return request.method == "DELETE" and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return str(obj.course_id) == view.kwargs.get("course_id")
