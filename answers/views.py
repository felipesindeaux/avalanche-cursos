from django.shortcuts import get_object_or_404
from rest_framework import generics

from questions.models import Question
from .models import Answer
from .serializers import AnswerSerializer, AnswerSerializerDetail

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ListCreateAnswerView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def perform_create(self, serializer):
        question_id = self.kwargs.get("question_id")
        question = get_object_or_404(Question, pk=question_id)
        serializer.save(user=self.request.user, question=question)
    
    def get_queryset(self):
        question_id = self.kwargs.get("question_id")
        get_object_or_404(Question, pk=question_id)
        return Answer.objects.filter(question_id=question_id)


class ListAnswerView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = AnswerSerializerDetail
    queryset = Answer.objects.all()

    def get_queryset(self):
        question_id = self.kwargs.get("question_id")
        get_object_or_404(Question, pk=question_id)

        answer_id = self.kwargs.get("answer_id")
        get_object_or_404(Answer, pk=answer_id)

        return Answer.objects.filter(question_id=question_id, id=answer_id)

