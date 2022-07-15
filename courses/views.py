from urllib import request
from students_lessons.serializers import StudentsLessonsSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from students.models import Student
from students.serializers import StudentsSerializer

from courses.mixins import SerializerByRoleMixin
from courses.models import Course
from lessons.models import Lesson
from courses.serializers import (
    CourseSerializer,
    RetrieveMyCoursesSerializer,
    UpdateStatusCourseSerializer,
)

from .permissions import (
    IsOwner,
    IsOwnerAndAdminToDelete,
    IsStudent,
    IsTeacherOrReadOnly,
    StudentHaventCourse,
)

from rest_framework.views import Response, status


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
    permission_classes = [IsAuthenticated, IsOwnerAndAdminToDelete]

    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class ListCoursesView(SerializerByRoleMixin, generics.ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_map = {True: RetrieveMyCoursesSerializer, False: StudentsSerializer}

    def get_queryset(self):
        if self.request.user.is_teacher:

            return Course.objects.filter(owner=self.request.user)

        else:
            router_parameter_gt = self.request.GET.get("completed")

        if router_parameter_gt:

            if router_parameter_gt == "completed":
                return Student.objects.filter(
                    student=self.request.user, is_completed=True
                )

            if router_parameter_gt == "uncompleted":
                return Student.objects.filter(
                    student=self.request.user, is_completed=False
                )

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
    permission_classes = [IsAuthenticatedOrReadOnly, IsStudent]

    def get_object(self, queryset=None):
        return get_object_or_404(
            Student,
            course__id=self.kwargs["course_id"],
            student=self.request.user,
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

        lessons = Lesson.objects.filter(course=course)
        if len(lessons) > 0:
            for lesson in lessons:
                serializer_lesson = StudentsLessonsSerializer(data={})
                serializer_lesson.is_valid(raise_exception=True)

                serializer_lesson.save(
                    student=self.request.user, course=course, lesson=lesson
                )

        serializer.save(student=self.request.user, course=course)
