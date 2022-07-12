from django.urls import path

from .views import (ListUsersView, LoginView, ManagementUserView, RegisterView,
                    RetrieveUpdateUserView)

urlpatterns = [
    path('signin/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('users/me/', RetrieveUpdateUserView.as_view()),
    path('users/', ListUsersView.as_view()),
    path('users/management/<id>/', ManagementUserView.as_view())
]
