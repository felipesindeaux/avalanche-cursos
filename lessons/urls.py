from django.urls import path

from . import views

urlpatterns = [
    path("courses/<str:course_id>/lessons/", views.ListCreateLessonView.as_view()),
    path(
        "courses/<str:course_id>/lessons/<str:pk>/",
        views.RetrieveUpdateDeleteLessonView.as_view(),
    ),
    path(
        "courses/<str:course_id>/lessons/<str:pk>/activate/", views.ActivateLessonView.as_view()
    ),
    path(
        "courses/<str:course_id>/lessons/<str:pk>/deactivate/",
        views.DeactivateLessonView.as_view(),
    ),
]
