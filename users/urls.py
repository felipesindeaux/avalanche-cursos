from django.urls import path

from .views import ListUsersView, LoginView, RegisterView, RetrieveUserView

urlpatterns = [
    path('signin/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('users/me/', RetrieveUserView.as_view()),
    path('users/', ListUsersView.as_view()),
]
