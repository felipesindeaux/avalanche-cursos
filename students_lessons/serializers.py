from os import read
from rest_framework import serializers


from courses.serializers import RetrieveMyCoursesSerializer
from users.serializers import UserSerializer
from lessons.serializers import LessonSerializer

from .models import StudentLessons


class StudentsLessonsSerializer(serializers.ModelSerializer):

    course = RetrieveMyCoursesSerializer(read_only=True)
    student = UserSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = StudentLessons
        fields = "__all__"
