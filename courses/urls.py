from django.urls import path

from . import views

urlpatterns = [
    path("courses/", views.CreateListCourseView.as_view()),
    path("courses/me", views.ListTeacherCoursesView.as_view()),
    path("courses/<pk>/", views.RetrieveUpdateDestroyView.as_view()),
    path("courses/activate/<pk>/", views.ActivateCourseView.as_view()),
    path("courses/deactivate/<pk>/", views.DeactivateCourseView.as_view())
]