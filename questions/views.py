from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Question
from .serializers import QuestionSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ListCreateQuestionView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ListQuestionView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(id=self.kwargs["question_id"])
