from django.urls import path

from .views import (ListUsersView, LoginView, RegisterView,
                    RetrieveUpdateUserView)

urlpatterns = [
    path('signin/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('users/me/', RetrieveUpdateUserView.as_view()),
    path('users/', ListUsersView.as_view()),
]
