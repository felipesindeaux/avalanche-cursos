from rest_framework import serializers

from lessons.models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(source="course.id", read_only=True)

    class Meta:
        model = Lesson

        exclude = ["course"]
