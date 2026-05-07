from django.urls import path
from .views import CreateCheckoutSession, stripe_webhook
from .views import payments_home
urlpatterns = [
    path('checkout/<int:course_id>/', CreateCheckoutSession.as_view()),
    path('webhook/', stripe_webhook),
path("", payments_home, name="payments_home"),
]

