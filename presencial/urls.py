from django.urls import path
from .views import PresencialSessionListCreateView, BookingCreateView

urlpatterns = [
    path('sessions/', PresencialSessionListCreateView.as_view()),
    path('sessions/<int:session_id>/book/', BookingCreateView.as_view()),
]

