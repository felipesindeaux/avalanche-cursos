from rest_framework import generics
from .models import Question
from .serializers import QuestionSerializer


class ListCreateQuestionView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

