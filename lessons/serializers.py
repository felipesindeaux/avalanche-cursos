from rest_framework import serializers

from lessons.models import Lesson
from tasks.models import Task


class LessonSerializer(serializers.ModelSerializer):
    course_id = serializers.UUIDField(source="course.id", read_only=True)
    tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Lesson

        exclude = ["course"]

        read_only_fields = ["is_active"]

    def get_tasks_count(self, instance):
        return Task.objects.filter(lesson_id=instance.id).count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        video = data.pop("video")
        if video:
            video_url_formatted = video[0 : video.index("?")]
            return {**data, "video_url": video_url_formatted}
        return data


class ToggleLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson

        fields = ["is_active"]

        read_only_fields = ["is_active"]
