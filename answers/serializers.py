from rest_framework import serializers

from users.serializers import UserSerializer
from questions.serializers import QuestionSerializer
from .models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = "__all__"

    def to_representation(self, instance):
        data = super(AnswerSerializer, self).to_representation(instance)
        data = {
            "id": data["id"],
            "answer": data["answer"],
            "date_published": data["date_published"],
            "updated_at": data["updated_at"],
            "question_id": data["question"]["id"],
            "user_id": data["user"]["id"],
        }
        return data


class AnswerSerializerDetail(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = "__all__"

    def to_representation(self, instance):
        data = super(AnswerSerializerDetail, self).to_representation(instance)
        data = {
            "id": data["id"],
            "answer": data["answer"],
            "date_published": data["date_published"],
            "updated_at": data["updated_at"],
            "question": data["question"],
            "user": data["user"],
        }
        return data


