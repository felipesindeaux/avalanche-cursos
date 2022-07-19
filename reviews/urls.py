from django.urls import path

from reviews.views import GetOrCreateReviewView, RetrieveReviewView

urlpatterns = [
    path("review/course/<uuid:course_id>/", GetOrCreateReviewView.as_view()),
    path("review/<uuid:pk>/", RetrieveReviewView.as_view()),
]
