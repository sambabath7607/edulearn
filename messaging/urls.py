from django.urls import path
from .views import RoomMessagesListView

urlpatterns = [
    path('rooms/<str:room_name>/messages/', RoomMessagesListView.as_view()),
]

