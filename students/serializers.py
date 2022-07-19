from courses.serializers import RetrieveMyCoursesSerializer
from rest_framework import serializers

from .models import Student


class StudentsSerializer(serializers.ModelSerializer):

    course = RetrieveMyCoursesSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'course', 'is_completed', 'student_id']
