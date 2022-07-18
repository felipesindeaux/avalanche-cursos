from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework import serializers
from lessons.models import Lesson

from users.serializers import UserNameSerializer

from .models import Course


class CourseSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True)
    owner = UserNameSerializer(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            **data,
            "categories": map(lambda data: data["name"], data["categories"]),
        }


class RetrieveMyCoursesSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True)
    owner = UserNameSerializer()
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"
        depth = 2

    def get_lessons_count(self, course: Course):
        return Lesson.objects.filter(course__id=course.id).count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            **data,
            "categories": map(
                lambda data: data["name"],
                data["categories"],
            ),
        }


class UpdateStatusCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["is_active"]
