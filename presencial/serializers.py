from rest_framework import serializers
from .models import PresencialSession, Booking

class PresencialSessionSerializer(serializers.ModelSerializer):
    remaining_places = serializers.SerializerMethodField()

    class Meta:
        model = PresencialSession
        fields = ['id', 'course', 'date', 'room', 'capacity', 'remaining_places']

    def get_remaining_places(self, obj):
        return obj.capacity - obj.bookings.count()


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'session', 'student', 'booked_at']
        read_only_fields = ['student', 'booked_at']
