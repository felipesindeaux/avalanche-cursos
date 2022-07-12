from attr import field
from .models import Course
from rest_framework import serializers

from users.serializers import AccountSerializer

class CourseSerializer(serializers.ModelSerializer):

    owner_id = AccountSerializer(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"
        depth = 2
