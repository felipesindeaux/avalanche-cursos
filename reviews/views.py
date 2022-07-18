from courses.models import Course
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from utils import get_object_or_404, validate_uuid

from reviews.models import Review
from reviews.permissions import IsReviewOwner, StudentHaveCourse
from reviews.serializers import ReviewSerializer


class GetOrCreateReviewView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, StudentHaveCourse]

    queryset = Review.objects.all()

    serializer_class = ReviewSerializer

    def perform_create(self, serializer):

        course = get_object_or_404(
            Course, "Course not found", id=self.kwargs['course_id'])

        serializer.save(user=self.request.user, course=course)

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        return Review.objects.filter(course__id=course_id)


class RetrieveReviewView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewOwner]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
