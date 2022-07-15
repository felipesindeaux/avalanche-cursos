from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework import serializers

from users.serializers import UserNameSerializer

from .models import Course


class CourseSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True)
    owner = UserNameSerializer(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "price",
            "total_hours",
            "date_published",
            "updated_at",
            "owner",
            "categories",
        ]

    def create(self, validated_data: dict):

        categories = validated_data.pop("categories")

        course = Course.objects.create(**validated_data)

        list_categories = []
        for category in categories:
            cat = Category.objects.get_or_create(**category)[0]
            list_categories.append(cat)

        course.categories.set(list_categories)

        return course

    def update(self, instance: Course, validated_data: dict):

        categories = validated_data.pop("categories", None)

        if categories:

            list_categories = []

            for cat in categories:
                cat_data = Category.objects.get_or_create(**cat)[0]
                list_categories.append(cat_data)

            instance.categories.set(list_categories)

        for key, value in validated_data.items():

            setattr(instance, key, value)

        instance.save()

        return instance

class RetrieveMyCoursesSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True)
    owner = UserNameSerializer()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "price",
            "total_hours",
            "date_published",
            "updated_at",
            "owner",
            "categories",
            "lessons"
        ]
        depth = 1


class UpdateStatusCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["is_active"]
