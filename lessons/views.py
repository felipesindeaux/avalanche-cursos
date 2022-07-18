from courses.models import Course
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response
from utils.get_object_or_404 import get_object_or_404
from utils.validate_uuid import validate_uuid

from .models import Lesson
from .serializers import LessonSerializer, ToggleLessonSerializer


class ListCreateLessonView(ListCreateAPIView):
    serializer_class = LessonSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_teacher or self.request.user.is_superuser:
            return Lesson.objects.filter(course_id=self.kwargs["course_id"])
        else:
            return Lesson.objects.filter(
                course_id=self.kwargs["course_id"], is_active=True
            )

    def perform_create(self, serializer):
        uuid = validate_uuid(self.kwargs["course_id"])

        course = get_object_or_404(Course, "Course not found", id=uuid)

        owner_id = course.owner.id
        authenticated_user_id = self.request.user.id

        if owner_id != authenticated_user_id:
            raise PermissionDenied("You must be the course owner to create a lesson")

        serializer.save(course=course)


class RetrieveUpdateDeleteLessonView(RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        lesson = self.get_object()

        course_id = str(lesson.course.id)
        course_id_param = self.kwargs["course_id"]

        if course_id != course_id_param:
            raise ParseError("Course does not own this lesson")

        owner_id = lesson.course.owner.id
        authenticated_user = self.request.user

        students = lesson.students.filter(student__student=authenticated_user)

        is_student = len(students) > 0
        is_owner = owner_id == authenticated_user.id
        is_admin = authenticated_user.is_superuser

        if not (is_owner or is_student or is_admin):
            raise PermissionDenied("You don't have access to view this lesson")

        serializer = self.get_serializer(lesson)

        return Response(serializer.data)

    def perform_update(self, serializer):
        lesson = self.get_object()

        course_id = str(lesson.course.id)
        course_id_param = self.kwargs["course_id"]

        if course_id != course_id_param:
            raise ParseError("Course does not own this lesson")

        owner_id = lesson.course.owner.id
        authenticated_user_id = self.request.user.id

        if owner_id != authenticated_user_id:
            raise PermissionDenied("You must be the course owner to update this lesson")

        serializer.save()

    def perform_destroy(self, instance):
        lesson = self.get_object()

        course_id = str(lesson.course.id)
        course_id_param = self.kwargs["course_id"]

        if course_id != course_id_param:
            raise ParseError("Course does not own this lesson")

        is_superuser = self.request.user.is_superuser

        if not is_superuser:
            raise PermissionDenied("You must be an admin to delete a lesson")

        instance.delete()


class ActivateLessonView(UpdateAPIView):
    serializer_class = ToggleLessonSerializer
    queryset = Lesson.objects.all()

    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        lesson = self.get_object()

        course_id = str(lesson.course.id)
        course_id_param = self.kwargs["course_id"]

        if course_id != course_id_param:
            raise ParseError("Course does not own this lesson")

        authenticated_user_id = self.request.user.id
        owner_id = lesson.course.owner.id

        if authenticated_user_id != owner_id:
            raise PermissionDenied("You must be the course owner to update this lesson")

        serializer.save(is_active=True)


class DeactivateLessonView(UpdateAPIView):
    serializer_class = ToggleLessonSerializer
    queryset = Lesson.objects.all()

    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        lesson = self.get_object()

        course_id = str(lesson.course.id)
        course_id_param = self.kwargs["course_id"]

        if course_id != course_id_param:
            raise ParseError("Course does not own this lesson")

        authenticated_user_id = self.request.user.id
        owner_id = lesson.course.owner.id

        if authenticated_user_id != owner_id:
            raise PermissionDenied("You must be the owner to update this lesson")

        serializer.save(is_active=False)
