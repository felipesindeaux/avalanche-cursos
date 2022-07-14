from courses.models import Course
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Lesson
from .permissions import (
    AdminDeletePermission,
    OwnerAdminStudentReadOnly,
    OwnerCreateUpdatePermission,
)
from .serializers import LessonSerializer


class ListCreateLessonView(ListCreateAPIView):
    serializer_class = LessonSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated & (OwnerAdminStudentReadOnly | OwnerCreateUpdatePermission)
    ]

    def get_queryset(self):
        if self.request.user.is_teacher or self.request.user.is_superuser:
            return Lesson.objects.filter(course_id=self.kwargs["course_id"])
        else:
            return Lesson.objects.filter(
                course_id=self.kwargs["course_id"], is_active=True
            )

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs["course_id"])

        serializer.save(course=course)


class RetrieveUpdateDeleteLessonView(RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    authentication_classes = [TokenAuthentication]

    permission_classes = [
        IsAuthenticated
        & (
            OwnerAdminStudentReadOnly
            | OwnerCreateUpdatePermission
            | AdminDeletePermission
        )
    ]
