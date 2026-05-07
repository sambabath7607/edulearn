from django.urls import path
from .views import RegisterView, LoginView, ProfileView
from .views import users_home
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
path("", users_home, name="users_home"),
]
