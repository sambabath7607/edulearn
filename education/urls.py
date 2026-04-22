from django.urls import path
from .views import CourseListView, CourseDetailView, LessonListView
from .views import EnrollView
from .views import (
    CourseListCreateView, CourseDetailView,
    LessonListCreateView, EnrollCourseView
)
from .views import MarkLessonCompleteView, CourseProgressView
urlpatterns = [
    path('', CourseListView.as_view()),
    path('<int:pk>/', CourseDetailView.as_view()),
    path('<int:course_id>/lessons/', LessonListView.as_view()),
    path('<int:course_id>/enroll/', EnrollView.as_view()),
    path('', CourseListCreateView.as_view()),
    path('<int:pk>/', CourseDetailView.as_view()),
    path('<int:course_id>/lessons/', LessonListCreateView.as_view()),
    path('<int:course_id>/enroll/', EnrollCourseView.as_view()),

]


urlpatterns += [
    path('lessons/<int:lesson_id>/complete/', MarkLessonCompleteView.as_view()),
    path('<int:course_id>/progress/', CourseProgressView.as_view()),
]
