from courses.models import Course
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response
from students_lessons.models import StudentLessons
from utils import get_object_or_404

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

        course = get_object_or_404(Course, "Course not found", id=self.kwargs["course_id"])

        owner_id = course.owner.id
        authenticated_user_id = self.request.user.id

        if owner_id != authenticated_user_id:
            raise PermissionDenied("You must be the course owner to create a lesson")

        lesson = serializer.save(course=course)

        if len(course.students.all()):
            lesson_students = [
                StudentLessons(student=student, lesson=lesson)
                for student in course.students.all()
            ]

            StudentLessons.objects.bulk_create(lesson_students)


class RetrieveUpdateDeleteLessonView(RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        lesson = self.get_object()

        owner_id = lesson.course.owner.id
        authenticated_user = self.request.user

        students = lesson.students_lessons.filter(student__student=authenticated_user)

        is_student = len(students) > 0
        is_owner = owner_id == authenticated_user.id
        is_admin = authenticated_user.is_superuser

        if not (is_owner or is_student or is_admin):
            raise PermissionDenied("You don't have access to view this lesson")

        serializer = self.get_serializer(lesson)

        return Response(serializer.data)

    def perform_update(self, serializer):
        lesson = self.get_object()

        owner_id = lesson.course.owner.id
        authenticated_user_id = self.request.user.id

        if owner_id != authenticated_user_id:
            raise PermissionDenied("You must be the course owner to update this lesson")

        serializer.save()

    def perform_destroy(self, instance):
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

        authenticated_user_id = self.request.user.id
        owner_id = lesson.course.owner.id

        if authenticated_user_id != owner_id:
            raise PermissionDenied("You must be the owner to update this lesson")

        serializer.save(is_active=False)
