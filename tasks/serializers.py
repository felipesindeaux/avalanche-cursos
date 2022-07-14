from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    lesson_id = serializers.IntegerField(source="lesson.id", read_only=True)

    class Meta:
        model = Task

        exclude = ["lesson"]
