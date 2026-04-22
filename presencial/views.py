from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PresencialSession, Booking
from .serializers import PresencialSessionSerializer, BookingSerializer


class PresencialSessionListCreateView(generics.ListCreateAPIView):
    queryset = PresencialSession.objects.all()
    serializer_class = PresencialSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # On suppose que seuls les teachers créent les sessions
        return serializer.save()


class BookingCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        try:
            session = PresencialSession.objects.get(id=session_id)
        except PresencialSession.DoesNotExist:
            return Response({"detail": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier la capacité
        if session.bookings.count() >= session.capacity:
            return Response({"detail": "No more places available"}, status=status.HTTP_400_BAD_REQUEST)

        booking, created = Booking.objects.get_or_create(
            session=session,
            student=request.user
        )

        if not created:
            return Response({"detail": "Already booked"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
