from lessons.models import Lesson
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from utils import get_object_or_404

from tasks.models import Task
from tasks.permissions import (HasCourseBond, HasCourseBondTaks,
                               IsTeacherOwner, IsTeacherOwnerTask)
from tasks.serializers import TaskSerializer, ToggleTaskSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Tasks'])
class ListCreateTaskView(ListCreateAPIView):
    serializer_class = TaskSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, (HasCourseBond | IsTeacherOwner)]

    def get_queryset(self):
        if self.request.user.is_teacher or self.request.user.is_superuser:
            return Task.objects.filter(lesson_id=self.kwargs["lesson_id"])
        else:
            return Task.objects.filter(
                lesson_id=self.kwargs["lesson_id"], is_active=True
            )

    def perform_create(self, serializer):

        lesson = get_object_or_404(

            Lesson, "Lesson not found", id=self.kwargs["lesson_id"])

        serializer.save(lesson=lesson)

@extend_schema(tags=['Tasks'])
class RetrieveUpdateDeleteTaskView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HasCourseBondTaks]

@extend_schema(tags=['Tasks'])
class ActivateTaskView(UpdateAPIView):
    serializer_class = ToggleTaskSerializer
    queryset = Task.objects.all()

    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated, IsTeacherOwnerTask]

    def perform_update(self, serializer):
        serializer.save(is_active=True)

@extend_schema(tags=['Tasks'])
class DeactivateTaskView(UpdateAPIView):
    serializer_class = ToggleTaskSerializer
    queryset = Task.objects.all()

    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated, IsTeacherOwnerTask]

    def perform_update(self, serializer):
        serializer.save(is_active=False)
