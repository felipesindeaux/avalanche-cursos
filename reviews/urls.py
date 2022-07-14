
from django.urls import path

from reviews.views import GetOrCreateReviewView, RetrieveReviewView

urlpatterns = [
    path('review/course/<int:id_course>/', GetOrCreateReviewView.as_view()),
    path('review/<int:id_review>', RetrieveReviewView.as_view()),
]