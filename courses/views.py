from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
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
    StudentHaventCourse,
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
    permission_classes = [IsAuthenticated, IsOwner, IsAdminToDelete]

    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class ListTeacherCoursesView(SerializerByRoleMixin, generics.ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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


class CompletCoursesView(generics.UpdateAPIView):
    serializer_class = StudentsSerializer
    queryset = Student.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, queryset=None):
        return get_object_or_404(
            Student, course__id=self.kwargs["course_id"], student=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(is_completed=True)


class BuyCoursesView(generics.CreateAPIView):
    serializer_class = StudentsSerializer
    queryset = Student.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsStudent, StudentHaventCourse]

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs["course_id"])
        serializer.save(student=self.request.user, course=course)
