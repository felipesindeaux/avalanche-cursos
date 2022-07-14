
from django.urls import path

from reviews.views import GetOrCreateReviewView, RetrieveReviewView

urlpatterns = [
    path('review/course/<id_course>/', GetOrCreateReviewView.as_view()),
    path('review/<pk>/', RetrieveReviewView.as_view()),
]
