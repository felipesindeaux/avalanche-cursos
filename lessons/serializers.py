from rest_framework import serializers
from students_lessons.models import StudentLessons
from tasks.models import Task
from tasks.serializers import TaskSerializer

from lessons.models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    course_id = serializers.UUIDField(source="course.id", read_only=True)
    tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Lesson

        fields = [
            "id",
            "course_id",
            "title",
            "description",
            "tasks_count",
            "video",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["is_active"]

    def get_tasks_count(self, instance):
        return Task.objects.filter(lesson_id=instance.id).count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        video = data.get("video", None)
        if video:
            video_url_formatted = video[0: video.index("?")]
            return {**data, "video": video_url_formatted}
        return data


class RetrieveLessonSerializer(serializers.ModelSerializer):
    course_id = serializers.UUIDField(source="course.id", read_only=True)
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Lesson

        fields = [
            "id",
            "course_id",
            "title",
            "description",
            "video",
            "is_active",
            "created_at",
            "updated_at",
            "tasks",
        ]

        read_only_fields = ["is_active"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        video = data.get("video", None)
        if video:
            video_url_formatted = video[0: video.index("?")]
            data = {**data, "video": video_url_formatted}
        return {
            **data,
            "tasks": map(
                lambda data: {"id": data["id"],
                              "title": data["title"]}, data["tasks"]
            ),
        }


class ToggleLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson

        fields = ["is_active"]

        read_only_fields = ["is_active"]


class ToggleCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentLessons

        fields = ["is_completed"]

        read_only_fields = ["is_completed"]
