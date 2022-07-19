from django.urls import path

from . import views

urlpatterns = [
    path("courses/", views.CreateListCourseView.as_view()),
    path("courses/me/", views.ListCoursesView.as_view()),
    path("courses/<uuid:pk>/", views.RetrieveUpdateDestroyView.as_view()),
    path("courses/buy/<uuid:course_id>/", views.BuyCoursesView.as_view()),
    path("courses/complete/<uuid:course_id>/", views.CompleteCoursesView.as_view()),
    path("courses/activate/<uuid:pk>/", views.ActivateCourseView.as_view()),
    path("courses/deactivate/<uuid:pk>/", views.DeactivateCourseView.as_view()),
]
