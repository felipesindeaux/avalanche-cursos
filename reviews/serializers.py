from rest_framework import serializers
from reviews.models import Review

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:

        model = Review

        fields = "__all__"

        read_only_fields = ["id"]

class ReviewListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review

        fields = "__all__"

        read_only_fields = ["id"]