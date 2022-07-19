from questions.serializers import QuestionSerializer
from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            "id",
            "content",
            "date_published",
            "updated_at",
            "question_id",
            "user_id",
        ]


class AnswerSerializerDetail(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "content", "date_published", "updated_at", "question", "user"]
