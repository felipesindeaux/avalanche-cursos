from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from courses.mixins import SerializerByRoleMixin

from courses.models import Course
from courses.serializers import CourseSerializer, UpdateStatusCourseSerializer
from students.models import Student
from students.serializers import StudentsSerializer

from .permissions import (
    IsAdminToDelete,
    IsOwner,
    IsStudent,
    IsTeacherOrReadOnly,
)


class CreateListCourseView(generics.ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsTeacherOrReadOnly]

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
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner, IsAdminToDelete]

    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class ListTeacherCoursesView(SerializerByRoleMixin, generics.ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_map = {True: CourseSerializer, False: StudentsSerializer}

    def get_queryset(self):
        if self.request.user.is_teacher:
            return Course.objects.filter(owner=self.request.user)
        else:
            return Student.objects.filter(student=self.request.user)


class ActivateCourseView(generics.UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    serializer_class = UpdateStatusCourseSerializer
    queryset = Course.objects.all()

    def perform_update(self, serializer):
        serializer.save(is_active=True)


class DeactivateCourseView(generics.UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    serializer_class = UpdateStatusCourseSerializer
    queryset = Course.objects.all()

    def perform_update(self, serializer):
        serializer.save(is_active=False)


class CompleteCoursesView(generics.UpdateAPIView):
    serializer_class = StudentsSerializer
    queryset = Student.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    lookup_field = "course__id"
    lookup_url_kwarg = "course_id"

    def perform_update(self, serializer):
        serializer.save(is_completed=True)


class BuyCoursesView(generics.CreateAPIView):
    serializer_class = StudentsSerializer
    queryset = Student.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsStudent]

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs["course_id"])
        serializer.save(student=self.request.user, course=course)
