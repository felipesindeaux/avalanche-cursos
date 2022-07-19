from courses.serializers import ListCourseSerializer
from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Student


class StudentsSerializer(serializers.ModelSerializer):

    course = ListCourseSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'course', 'is_completed', 'student_id']
