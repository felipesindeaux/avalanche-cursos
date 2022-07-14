from rest_framework import serializers
from courses.serializers import CourseSerializer
from reviews.models import Review
from users.serializers import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    
    class Meta:

        model = Review

        fields = "__all__"

        read_only_fields = ["id"]

        depth = 1


    def to_representation(self, instance):
            data = super(ReviewSerializer, self).to_representation(instance)
            data = {"id": data['id'], "score": data['score'], "comment": data['comment'], "user_id": data['user']['id'], "course_id": data['course']['id']
            , "date_published": data['date_published'], "updated_at": data['updated_at']
            }
            return data



class ReviewListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review

        fields = "__all__"

        read_only_fields = ["id"]

        depth = 1

        

    def to_representation(self, instance):
            data = super(ReviewListSerializer, self).to_representation(instance)
            data = {
            "id": data['id'], "score": data['score'], "comment": data['comment'], 
            "user_id": data['user']['id'], "course_id": data['course']['id'], "date_published": data['date_published'], "updated_at": data['updated_at']
            }
            return data
