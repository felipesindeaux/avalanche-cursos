from django.urls import path

from . import views

urlpatterns = [
    path("courses/", views.CreateListCourseView.as_view()),
    path("courses/me/", views.ListTeacherCoursesView.as_view()),
    path("courses/<pk>/", views.RetrieveUpdateDestroyView.as_view()),
    path("courses/buy/<course_id>/", views.BuyCoursesView.as_view()),
    path("courses/complete/<course_id>/", views.CompletCoursesView.as_view()),
    path("courses/activate/<course_id>/", views.ActivateCourseView.as_view()),
    path("courses/deactivate/<pk>/", views.DeactivateCourseView.as_view()),
]
