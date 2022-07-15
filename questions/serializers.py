from rest_framework import serializers

from users.serializers import UserIdSerializer
from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    user = UserIdSerializer(read_only=True)

    class Meta:
        model = Question
        fields = "__all__"

    def to_representation(self, instance):
        data = super(QuestionSerializer, self).to_representation(instance)
        data = {
            "id": data["id"],
            "title": data["title"],
            "description": data["description"],
            "date_published": data["date_published"],
            "updated_at": data["updated_at"],
            "user_id": data["user"]["id"],
        }
        return data



