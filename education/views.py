from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Enrollment, Course
from .serializers import EnrollmentSerializer

from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from .models import LessonProgress, Lesson, Course

class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Lesson.objects.filter(course_id=course_id)


class EnrollView(APIView):
    def post(self, request, course_id):
        course = Course.objects.get(id=course_id)
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course
        )
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=201)


class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsTeacher()]
        return []

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course_id'])

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs['course_id'])
class EnrollCourseView(APIView):
    def post(self, request, course_id):
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course_id=course_id
        )
        return Response(EnrollmentSerializer(enrollment).data)


class MarkLessonCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_id):
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"detail": "Lesson not found"}, status=404)

        progress, created = LessonProgress.objects.get_or_create(
            student=request.user,
            lesson=lesson
        )
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()

        return Response(LessonProgressSerializer(progress).data, status=200)
class CourseProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found"}, status=404)

        lessons = course.lessons.all()
        total = lessons.count()

        if total == 0:
            return Response({"progress": 0, "total_lessons": 0, "completed_lessons": 0})

        completed = LessonProgress.objects.filter(
            student=request.user,
            lesson__in=lessons,
            completed=True
        ).count()

        progress_percent = int((completed / total) * 100)

        return Response({
            "course": course.title,
            "total_lessons": total,
            "completed_lessons": completed,
            "progress": progress_percent
        })
