from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from courses.models import Course
from courses.serializers import CourseSerializer, UpdateStatusCourseSerializer

from .permissions import IsAdminToDelete, IsTeacher


class CreateListCourseView(generics.ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = CourseSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Course.objects.all()
        else:
            return Course.objects.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminToDelete]

    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class ListTeacherCoursesView(generics.ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsTeacher]

    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)


class ActivateCourseView(generics.UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    serializer_class = UpdateStatusCourseSerializer
    queryset = Course.objects.all()

    def perform_update(self, serializer):
        serializer.save(is_active=True)


class DeactivateCourseView(generics.UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    serializer_class = UpdateStatusCourseSerializer
    queryset = Course.objects.all()

    def perform_update(self, serializer):
        serializer.save(is_active=False)
