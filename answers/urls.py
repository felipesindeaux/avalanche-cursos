from django.urls import path

from . import views

urlpatterns = [
    path('questions/<question_id>/answers/', views.ListCreateAnswerView.as_view()),
    path('questions/<question_id>/answers/<answer_id>/', views.ListAnswerView.as_view()),
    
]
