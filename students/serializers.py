from rest_framework import serializers

from courses.serializers import CourseSerializer
from users.serializers import UserSerializer

from .models import Student


class StudentsSerializer(serializers.ModelSerializer):

    course = CourseSerializer(read_only=True)
    student = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = "__all__"
