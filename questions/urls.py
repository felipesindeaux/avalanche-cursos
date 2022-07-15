from django.urls import path

from . import views

urlpatterns = [
    path('questions/', views.ListCreateQuestionView.as_view()),
    path('questions/<question_id>/', views.ListQuestionView.as_view()),
]
