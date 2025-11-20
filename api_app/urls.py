# backend/api_app/urls.py
from django.urls import path
from .views import AskAPIView, FeedbackAPIView, AnalyticsAPIView

urlpatterns = [
    path('ask/', AskAPIView.as_view(), name='ask'),
    path('feedback/', FeedbackAPIView.as_view(), name='feedback'),
    path('analytics/', AnalyticsAPIView.as_view(), name='analytics'),
]
