from django.urls import path

from . import views

urlpatterns = [
    path("courses/", views.CreateListCourseView.as_view()),
    path("courses/me/", views.ListCoursesView.as_view()),
    path("courses/<str:pk>/", views.RetrieveUpdateDestroyView.as_view()),
    path("courses/buy/<str:course_id>/", views.BuyCoursesView.as_view()),
    path("courses/complete/<str:course_id>/", views.CompleteCoursesView.as_view()),
    path("courses/activate/<str:pk>/", views.ActivateCourseView.as_view()),
    path("courses/deactivate/<str:pk>/", views.DeactivateCourseView.as_view()),
]
