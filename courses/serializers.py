from categories.models import Category

from categories.serializers import CategorySerializer
from .models import Course
from rest_framework import serializers

from users.serializers import AccountSerializer

class CourseSerializer(serializers.ModelSerializer):

    owner = AccountSerializer(read_only=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Course
        fields = "__all__"
        depth = 2
    
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
        non_editable_keys = ("is_active",)
        categories = validated_data.pop("categories", None)

        if categories:

            list_categories = []

            for cat in categories:
                cat_data = Category.objects.get_or_create(**cat)[0]
                list_categories.append(cat_data)

            instance.categories.set(list_categories)

        for key, value in validated_data.items():
            if key in non_editable_keys:
                raise KeyError(f"You can not update {key} property.")
            setattr(instance, key, value)

        instance.save()

        return instance


    

class UpdateStatusCourseSerializer(serializers.ModelSerializer):
    owner = AccountSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"
        depth = 2
        read_only_fields = [
            "title",
            "description",
            "price",
            "total_hours",
            "date_published",
            "updated_at",
            "is_active",
        ] 