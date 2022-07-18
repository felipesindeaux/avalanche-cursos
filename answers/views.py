from django.shortcuts import get_object_or_404
from rest_framework import generics
from answers.permissions import IsOwnerAndAdminToDelete

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


class RetrieveUpdateDestroyAnswerView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerAndAdminToDelete]

    serializer_class = AnswerSerializerDetail
    queryset = Answer.objects.all()

    lookup_url_kwarg = "answer_id"

    



