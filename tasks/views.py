from drf_spectacular.utils import extend_schema
from lessons.models import Lesson
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils import get_object_or_404

from tasks import permissions
from tasks.models import Task
from tasks.serializers import TaskSerializer, ToggleTaskSerializer


@extend_schema(tags=["Tasks"])
class ListCreateTaskView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
        (permissions.HasCourseBond | permissions.IsTeacherOwner),
    ]

    def get_queryset(self):
        if self.request.user.is_teacher or self.request.user.is_superuser:
            return Task.objects.filter(lesson_id=self.kwargs["lesson_id"])
        else:
            return Task.objects.filter(
                lesson_id=self.kwargs["lesson_id"], is_active=True
            )

    def perform_create(self, serializer):

        lesson = get_object_or_404(
            Lesson, "Lesson not found", id=self.kwargs["lesson_id"]
        )

        serializer.save(lesson=lesson)


@extend_schema(tags=["Tasks"])
class RetrieveUpdateDeleteTaskView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, permissions.HasCourseBondTaks]


@extend_schema(tags=["Tasks"])
class ActivateTaskView(generics.UpdateAPIView):
    serializer_class = ToggleTaskSerializer
    queryset = Task.objects.all()

    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated, permissions.IsTeacherOwnerTask]

    def perform_update(self, serializer):
        serializer.save(is_active=True)


@extend_schema(tags=["Tasks"])
class DeactivateTaskView(generics.UpdateAPIView):
    serializer_class = ToggleTaskSerializer
    queryset = Task.objects.all()

    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated, permissions.IsTeacherOwnerTask]

    def perform_update(self, serializer):
        serializer.save(is_active=False)
