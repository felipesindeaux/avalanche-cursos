from django.urls import path

from . import views

urlpatterns = [
    path(
        "lessons/<uuid:lesson_id>/tasks/",
        views.ListCreateTaskView.as_view(),
    ),
    path(
        "tasks/<uuid:pk>/",
        views.RetrieveUpdateDeleteTaskView.as_view(),
    ),
    path(
        "tasks/<uuid:pk>/activate/",
        views.ActivateTaskView.as_view(),
    ),
    path(
        "tasks/<uuid:pk>/deactivate/",
        views.DeactivateTaskView.as_view(),
    ),
]
