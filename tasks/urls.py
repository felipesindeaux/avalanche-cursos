from django.urls import path

from . import views

urlpatterns = [
    path(
        "courses/<course_id>/lessons/<lesson_id>/tasks/",
        views.ListCreateTaskView.as_view(),
    ),
    path(
        "courses/<course_id>/lessons/<lesson_id>/tasks/<pk>/",
        views.RetrieveUpdateDeleteTaskView.as_view(),
    ),
    path(
        "courses/<course_id>/lessons/<lesson_id>/tasks/<pk>/activate/",
        views.ActivateTaskView.as_view(),
    ),
    path(
        "courses/<course_id>/lessons/<lesson_id>/tasks/<pk>/deactivate/",
        views.DeactivateTaskView.as_view(),
    ),
]
