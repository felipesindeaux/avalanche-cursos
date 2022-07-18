from django.urls import path

from . import views

urlpatterns = [
    path('questions/<question_id>/answers/', views.ListCreateAnswerView.as_view()),
    path('questions/answers/<answer_id>/', views.RetrieveUpdateDestroyAnswerView.as_view()),
    
]
