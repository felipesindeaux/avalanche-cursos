from rest_framework import serializers

from lessons.models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson

        fields = "__all__"

        read_only_fields = ['id', 'is_active', "created_at", "updated_at"]
