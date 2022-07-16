from django.urls import path

from . import views

urlpatterns = [
    path('questions/', views.ListCreateQuestionView.as_view()),
    path('questions/<uuid:question_id>/', views.RetrieveUpdateDestroyQuestionView.as_view()),
]
