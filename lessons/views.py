from courses.models import Course
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Lesson
from .permissions import (IsAdminDelete, IsOwner, IsOwnerUpdate,
                          IsStudentRetrieve)
from .serializers import LessonSerializer


class CreateLessonView(CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated & IsOwner]

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs["course_id"])

        serializer.save(course=course)


class RetrieveUpdateDeleteLessonView(RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    authentication_classes = [TokenAuthentication]

    permission_classes = [
        IsAuthenticated & (IsStudentRetrieve | IsOwnerUpdate | IsAdminDelete)
    ]
