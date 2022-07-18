from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from lessons.models import Lesson
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from students.models import Student
from students.serializers import StudentsSerializer
from students_lessons.models import StudentLessons

from courses.mixins import SerializerByMethodMixin
from courses.models import Course
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


class ListCoursesView(SerializerByMethodMixin, generics.ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RetrieveMyCoursesSerializer
    serializer_map = {
        "Teacher": RetrieveMyCoursesSerializer,
        "Student": StudentsSerializer,
    }

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_teacher:
            router_parameter_gt = self.request.GET.get("active")

            if router_parameter_gt:

                if router_parameter_gt == "true":
                    return Course.objects.filter(
                        owner=self.request.user, is_active=True
                    )

                if router_parameter_gt == "false":
                    return Course.objects.filter(
                        owner=self.request.user, is_active=False
                    )

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

        student_courses = serializer.save(student=self.request.user, course=course)

        lessons = Lesson.objects.filter(course=course)

        if len(lessons):
            lesson_students = [
                StudentLessons(student=student_courses, lesson=lesson)
                for lesson in lessons
            ]

            StudentLessons.objects.bulk_create(lesson_students)
