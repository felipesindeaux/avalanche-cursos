from django.shortcuts import get_object_or_404
from rest_framework import serializers
from answers.models import Answer

from users.serializers import UserIdSerializer
from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    user = UserIdSerializer(read_only=True)
    
    answers_count = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = "__all__"


    def get_answers_count(self, question: Question):
        answers_count = Answer.objects.filter(question_id=question.id).count()
        return answers_count

    def to_representation(self, instance):
        data = super(QuestionSerializer, self).to_representation(instance)
        data = {
            "id": data["id"],
            "title": data["title"],
            "description": data["description"],
            "answers_count": data["answers_count"],
            "date_published": data["date_published"],
            "updated_at": data["updated_at"],
            "user_id": data["user"]["id"],
        }
        return data
