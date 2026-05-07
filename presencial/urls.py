from django.urls import path
from .views import PresencialSessionListCreateView, BookingCreateView
from .views import presencial_home

urlpatterns = [
    path('sessions/', PresencialSessionListCreateView.as_view()),
    path('sessions/<int:session_id>/book/', BookingCreateView.as_view()),
    path("", presencial_home, name="presencial_home"),

    path("", presencial_home, name="payments_home"),

]

