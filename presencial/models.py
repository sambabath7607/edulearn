from django.db import models
from education.models import Course
from users.models import User

class PresencialSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='presencial_sessions')
    date = models.DateTimeField()
    room = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f"{self.course.title} - {self.date}"
class Booking(models.Model):
    session = models.ForeignKey(PresencialSession, on_delete=models.CASCADE, related_name='bookings')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'student')

    def __str__(self):
        return f"{self.student.username} → {self.session}"
from django.db import models
from users.models import User
from education.models import Course

class PresencialSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='presencial_sessions')
    date = models.DateTimeField()
    room = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f"{self.course.title} - {self.date} ({self.room})"


class Booking(models.Model):
    session = models.ForeignKey(PresencialSession, on_delete=models.CASCADE, related_name='bookings')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'student')

    def __str__(self):
        return f"{self.student.username} → {self.session}"
