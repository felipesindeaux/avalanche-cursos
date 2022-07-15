
from django.urls import path

from reviews.views import GetOrCreateReviewView, RetrieveReviewView

urlpatterns = [
    path('review/course/<str:course_id>/', GetOrCreateReviewView.as_view()),
    path('review/<str:pk>/', RetrieveReviewView.as_view()),
]
