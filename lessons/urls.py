from django.urls import path

from . import views

urlpatterns = [
    path("courses/<uuid:course_id>/lessons/", views.ListCreateLessonView.as_view()),
    path(
        "lessons/<uuid:pk>/",
        views.RetrieveUpdateDeleteLessonView.as_view(),
    ),
    path("lessons/<uuid:pk>/activate/", views.ActivateLessonView.as_view()),
    path(
        "lessons/<uuid:pk>/deactivate/",
        views.DeactivateLessonView.as_view(),
    ),
]
