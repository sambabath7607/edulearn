from django.db import models
from users.models import User

class Course(models.Model):
    MODE_CHOICES = (
        ('online', 'Online'),
        ('presencial', 'Presencial'),
        ('hybrid', 'Hybrid'),
    )

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='online')
    level = models.CharField(max_length=50, default='beginner')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    video_url = models.URLField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.course.title} - {self.title}"
class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} → {self.course.title}"
class LiveSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='live_sessions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    meeting_link = models.URLField()

    def __str__(self):
        return f"Live: {self.course.title} - {self.start_time}"

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    student = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('education.Course', on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} → {self.course.title}"

class Lesson(models.Model):
    course = models.ForeignKey('education.Course', on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    video_url = models.URLField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.course.title} - {self.title}"
from django.utils import timezone

class LessonProgress(models.Model):
    student = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey('education.Lesson', on_delete=models.CASCADE, related_name='progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student.username} - {self.lesson.title} ({'done' if self.completed else 'pending'})"
