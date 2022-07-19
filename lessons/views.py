from courses.models import Course
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response
from students.models import Student
from students_lessons.models import StudentLessons
from utils import get_object_or_404

from . import serializers
from .models import Lesson


@extend_schema(tags=["Lessons"])
class ListCreateLessonView(generics.ListCreateAPIView):
    serializer_class = serializers.LessonSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        authenticated_user = self.request.user
        course_id = self.kwargs["course_id"]

        if authenticated_user.is_teacher or authenticated_user.is_superuser:
            return Lesson.objects.filter(course_id=course_id)
        else:
            is_completed_param = self.request.GET.get("completed")

            if not is_completed_param:
                return Lesson.objects.filter(
                    course_id=self.kwargs["course_id"], is_active=True
                )

            student = get_object_or_404(
                Student,
                "You did not buy this course",
                student=authenticated_user.id,
                course=course_id,
            )

            is_completed = True if is_completed_param == "true" else False

            student_lessons = student.lessons.filter(is_completed=is_completed)

            return [
                student_lesson.lesson
                for student_lesson in student_lessons
                if student_lesson.lesson.is_active
            ]

    def perform_create(self, serializer):

        course = get_object_or_404(
            Course, "Course not found", id=self.kwargs["course_id"]
        )

        owner_id = course.owner.id
        authenticated_user_id = self.request.user.id

        if owner_id != authenticated_user_id:
            raise PermissionDenied("You must be the course owner to create a lesson")

        lesson = serializer.save(course=course)

        all_course_students = course.students.all()

        if len(all_course_students):

            for student in all_course_students:

                email_html = get_template("email_template.html")
                email_context = {
                    "student_name": student.student.name.title(),
                    "course_name": course.title.title(),
                    "lesson_name": lesson.title.title(),
                }

                email = EmailMultiAlternatives(
                    f"Novo lição de {course.title.title()} 🏔",
                    strip_tags(render_to_string("email_template.html", email_context)),
                    None,
                    [student.student.email],
                )

                email.attach_alternative(email_html.render(email_context), "text/html")
                email.send()

            lesson_students = [
                StudentLessons(student=student, lesson=lesson)
                for student in course.students.all()
            ]

            StudentLessons.objects.bulk_create(lesson_students)


@extend_schema(tags=["Lessons"])
class RetrieveUpdateDeleteLessonView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.RetrieveLessonSerializer
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


@extend_schema(tags=["Lessons"])
class ActivateLessonView(generics.UpdateAPIView):
    serializer_class = serializers.ToggleLessonSerializer
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


@extend_schema(tags=["Lessons"])
class DeactivateLessonView(generics.UpdateAPIView):
    serializer_class = serializers.ToggleLessonSerializer
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


class CompleteLessonView(generics.UpdateAPIView):
    serializer_class = serializers.ToggleCompletedSerializer
    queryset = Lesson.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        lesson = get_object_or_404(Lesson, "Lesson not found", pk=self.kwargs["pk"])

        lesson.students_lessons.filter

        course_id = lesson.course.id

        student = get_object_or_404(
            Student,
            "You did not buy this course",
            student=self.request.user.id,
            course=course_id,
        )

        return student.lessons.get(lesson=lesson.id)

    def perform_update(self, serializer):
        serializer.save(is_completed=True)
