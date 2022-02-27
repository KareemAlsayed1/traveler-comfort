from django.urls import path
from .views import next_question

urlpatterns = [
    path('next-question/', next_question.as_view())
]