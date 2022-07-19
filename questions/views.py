from django.shortcuts import get_object_or_404
from rest_framework import generics

from questions.permissions import IsOwnerAndAdminToDelete
from .models import Question
from .serializers import QuestionSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ListCreateQuestionView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        router_parameter_gt = self.request.GET.get("category")

        if router_parameter_gt:
            return Question.objects.filter(
                categories__name__contains=router_parameter_gt
            )

        return Question.objects.all()


class RetrieveUpdateDestroyQuestionView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerAndAdminToDelete]

    serializer_class = QuestionSerializer
    lookup_url_kwarg = "question_id"

    def get_queryset(self):
        id = self.kwargs.get("question_id")
        get_object_or_404(Question, pk=id)
        return Question.objects.filter(id=id)