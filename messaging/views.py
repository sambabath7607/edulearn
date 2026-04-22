from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer

class RoomMessagesListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_name = self.kwargs['room_name']
        return Message.objects.filter(room__name=room_name)
