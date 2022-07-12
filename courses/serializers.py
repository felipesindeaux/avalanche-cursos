from unicodedata import category
from attr import field

from categories.serializers import CategorySerializer
from .models import Course
from rest_framework import serializers

from users.serializers import AccountSerializer

class CourseSerializer(serializers.ModelSerializer):

    owner_id = AccountSerializer(read_only=True)
    category = CategorySerializer(many=True)

    class Meta:
        model = Course
        fields = "__all__"
        depth = 2

    

class UpdateStatusCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        depth = 2
        read_only_fields = "__all__"