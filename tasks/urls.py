from django.urls import path

from . import views

urlpatterns = [
    path(
        "courses/<str:course_id>/lessons/<str:lesson_id>/tasks/",
        views.ListCreateTaskView.as_view(),
    ),
    path(
        "courses/<str:course_id>/lessons/<str:lesson_id>/tasks/<str:pk>/",
        views.RetrieveUpdateDeleteTaskView.as_view(),
    ),
    path(
        "courses/<str:course_id>/lessons/<str:lesson_id>/tasks/<str:pk>/activate/",
        views.ActivateTaskView.as_view(),
    ),
    path(
        "courses/<str:course_id>/lessons/<str:lesson_id>/tasks/<str:pk>/deactivate/",
        views.DeactivateTaskView.as_view(),
    ),
]
