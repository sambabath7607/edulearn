from django.urls import path
from .views import CreateCheckoutSession, stripe_webhook

urlpatterns = [
    path('checkout/<int:course_id>/', CreateCheckoutSession.as_view()),
    path('webhook/', stripe_webhook),
]
