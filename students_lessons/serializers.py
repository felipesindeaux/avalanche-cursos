from os import read

from lessons.serializers import LessonSerializer
from rest_framework import serializers
from students.serializers import StudentsSerializer

from .models import StudentLessons


class StudentsLessonsSerializer(serializers.ModelSerializer):

    student = StudentsSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)

    class Meta:
        model = StudentLessons
        fields = "__all__"
