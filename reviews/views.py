from courses.models import Course
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from utils import get_object_or_404, validate_uuid

from reviews.models import Review
from reviews.permissions import IsReviewOwner
from reviews.serializers import ReviewSerializer

# Create your views here.


class GetOrCreateReviewView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Review.objects.all()

    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        uuid = validate_uuid(self.kwargs["course_id"])

        course = get_object_or_404(Course, "Course not found", id=uuid)

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
