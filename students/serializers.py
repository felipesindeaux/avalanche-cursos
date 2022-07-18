from rest_framework import serializers

from courses.serializers import RetrieveMyCoursesSerializer
from users.serializers import UserSerializer

from .models import Student


class StudentsSerializer(serializers.ModelSerializer):

    course = RetrieveMyCoursesSerializer(read_only=True)
    student = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        student = data.pop("student")
        return {
            **data,
            "student_id": student["id"],
        }
