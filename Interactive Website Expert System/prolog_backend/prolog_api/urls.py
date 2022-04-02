from django.urls import path
from .views import next_question

# Add the URL for the API
urlpatterns = [
    path('next-question/', next_question.as_view())
]