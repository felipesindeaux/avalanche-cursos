from answers.models import Answer
from categories.models import Category
from categories.serializers import CategorySerializer
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.serializers import UserIdSerializer

from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    user = UserIdSerializer(read_only=True)
    categories = CategorySerializer(many=True)

    answers_count = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = "__all__"
        depth = 1

    def create(self, validated_data: dict):

        categories = validated_data.pop("categories")

        question = Question.objects.create(**validated_data)

        list_categories = []
        for category in categories:
            cat = Category.objects.get_or_create(**category)[0]
            list_categories.append(cat)

        question.categories.set(list_categories)

        return question

    def update(self, instance: Question, validated_data: dict):

        categories = validated_data.pop("categories", None)

        if categories:

            list_categories = []

            for cat in categories:
                cat_data = Category.objects.get_or_create(**cat)[0]
                list_categories.append(cat_data)

            instance.categories.set(list_categories)

        for key, value in validated_data.items():

            setattr(instance, key, value)

        instance.save()

        return instance

    def get_answers_count(self, question: Question):
        answers_count = Answer.objects.filter(question_id=question.id).count()
        return answers_count

    def to_representation(self, instance):
        data = super(QuestionSerializer, self).to_representation(instance)
        categories = map(lambda data: data['name'], data['categories'])
        data = {
            "id": data["id"],
            "title": data["title"],
            "description": data["description"],
            "answers_count": data["answers_count"],
            "date_published": data["date_published"],
            "updated_at": data["updated_at"],
            "user_id": data["user"]["id"],
            "categories": categories,
        }
        return data
