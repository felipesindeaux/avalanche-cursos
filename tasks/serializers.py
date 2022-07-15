from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    lesson_id = serializers.UUIDField(source="lesson.id", read_only=True)

    class Meta:
        model = Task

        exclude = ["lesson"]

        read_only_fields = ["is_active"]


class ToggleTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task

        fields = ["is_active"]

        read_only_fields = ["is_active"]
