from rest_framework import generics

from reviews.models import Review
from reviews.mixins import MapMathodsMixin
from reviews.serializers import ReviewListSerializer, ReviewSerializer
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class GetOrCreateReviewView(MapMathodsMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]

    queryset = Review.objects.all()

    serializer_map = {
        "GET": ReviewListSerializer,
        "POST": ReviewSerializer
    }

    def perform_create(self, serializer):
       serializer.save(seller=self.request.user)


class RetrieveReviewView(MapMathodsMixin, generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]

    queryset = Review.objects.all()

    serializer_map = {
        "GET": ReviewListSerializer,
        "POST": ReviewSerializer,
        "PATCH": ReviewSerializer,
        "DELETE": ReviewListSerializer
    }