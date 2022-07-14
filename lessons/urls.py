from django.urls import path

from . import views

urlpatterns = [
    path("courses/<course_id>/lessons/", views.ListCreateLessonView.as_view()),
    path(
        "courses/<course_id>/lessons/<pk>/",
        views.RetrieveUpdateDeleteLessonView.as_view(),
    ),
]
