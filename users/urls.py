from django.urls import include, path

from . import views

urlpatterns = [
    path("signin/", views.LoginView.as_view()),
    path("register/", views.RegisterView.as_view()),
    path("users/me/", views.RetrieveUpdateUserView.as_view()),
    path("users/", views.ListUsersView.as_view()),
    path("users/management/<uuid:id>/", views.ManagementUserView.as_view()),
    path(
        "users/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]
