from django.shortcuts import render

# Create your views here.
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Transaction
from education.models import Course

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSession(APIView):
    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found"}, status=404)

        # Créer une transaction en attente
        transaction = Transaction.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            status='pending'
        )

        # Créer la session Stripe
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'cad',
                    'product_data': {
                        'name': course.title,
                    },
                    'unit_amount': int(course.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url="http://localhost:8000/payment-success/",
            cancel_url="http://localhost:8000/payment-cancel/",
        )

        transaction.stripe_session_id = session.id
        transaction.save()

        return Response({"checkout_url": session.url})
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = "ta_clé_webhook"

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        transaction = Transaction.objects.filter(stripe_session_id=session['id']).first()
        if transaction:
            transaction.status = 'paid'
            transaction.save()

    return HttpResponse(status=200)
