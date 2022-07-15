from django.shortcuts import get_object_or_404
from rest_framework import generics

from reviews.models import Review
from reviews.serializers import ReviewSerializer
from rest_framework.authentication import TokenAuthentication
from courses.models import Course
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.permissions import IsReviewOwner

# Create your views here.

class GetOrCreateReviewView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Review.objects.all()

    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
       course_id = self.kwargs.get("course_id")
       course = get_object_or_404(Course, pk=course_id)
       
       serializer.save(user=self.request.user, course=course)

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        get_object_or_404(Course, pk=course_id)
        return Review.objects.filter(course__id=course_id)


class RetrieveReviewView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewOwner]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer