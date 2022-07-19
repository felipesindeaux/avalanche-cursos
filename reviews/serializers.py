from rest_framework import serializers

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review

        fields = ['id', 'score', 'comment', 'date_published',
                  'updated_at', 'user_id', 'course_id']
