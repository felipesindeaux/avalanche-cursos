from django.urls import path

from . import views

urlpatterns = [
    path('questions/<uuid:question_id>/answers/',
         views.ListCreateAnswerView.as_view()),
    path('questions/answers/<uuid:answer_id>/',
         views.RetrieveUpdateDestroyAnswerView.as_view()),

]
