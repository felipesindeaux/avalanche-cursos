from django.urls import include, path

from .views import (ListUsersView, LoginView, ManagementUserView, RegisterView,
                    RetrieveUpdateUserView)

urlpatterns = [
    path('signin/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('users/me/', RetrieveUpdateUserView.as_view()),
    path('users/', ListUsersView.as_view()),
    path('users/management/<str:id>/', ManagementUserView.as_view()),
    path(
        "users/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset")
    )
]
