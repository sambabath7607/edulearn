from django.urls import path
from .views import RoomMessagesListView
from .views import messaging_home
urlpatterns = [
    path('rooms/<str:room_name>/messages/', RoomMessagesListView.as_view()),
    path("", messaging_home, name="messaging_home"),
]

