import requests
from django.conf import settings 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework .response import Response
from rest_framework.generics import GenericAPIView
from app.orders.models import Order,Status
from ..models import Payment,PaymentStatus
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from django.db import transaction
# Create your views here.
from .serializer import PaymentInitiateSerializer

class PaymentInitiateView(GenericAPIView):
    serializer_class = PaymentInitiateSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Payment",
        tags=["Payments"]
    )
    def post(self, request, *args, **kwargs):
        order_id = request.data.get("order_id")

        order = get_object_or_404(
            Order.objects.filter(user=request.user),
            pk=order_id,
        )

        if order.status != Status.PENDING:
            return Response(
                {"detail": "This order is not eligible for payment."},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment = Payment.objects.create(
            order=order,
            total_amount=order.total_amount,
        )

        amount_paisa = int(payment.total_amount * 100)

        payload = {
            "return_url": "http://127.0.0.1:8000/api/payments/verify/",
            "website_url": "http://127.0.0.1:8000",
            "amount": amount_paisa,
            "purchase_order_id": str(order.id),
            "purchase_order_name": f"Order {order.id}",
        }

        khalti_response = requests.post(
            "https://dev.khalti.com/api/v2/epayment/initiate/",
            headers={
                "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )

        if khalti_response.status_code != 200:
            return Response(
                {"detail": "Unable to initiate Khalti payment."},
                status=status.HTTP_502_BAD_GATEWAY
            )

        response_data = khalti_response.json()

        pidx = response_data["pidx"]
        payment_url = response_data["payment_url"]

        payment.pidx = pidx
        payment.status = PaymentStatus.INITIATED
        payment.save()

        return Response({
            "payment_url": payment_url,
            "pidx": pidx,
        })
    
class PaymentVerifyView(GenericAPIView):
    @extend_schema(
            summary="PaymentVerify",
            tags=["Payments"]
        )
    def get(self, request, *args, **kwargs):
        pidx = request.query_params.get("pidx")

        if not pidx:
            return Response(
                {"detail": "Missing payment identifier"},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment = get_object_or_404(
            Payment.objects.filter(pidx=pidx)
        )

        # Check if payment is already completed
        if payment.status == PaymentStatus.COMPLETED:
            return Response(
                {"detail": "Payment is already completed."},
                status=status.HTTP_200_OK
            )

        # Contact Khalti
        try:
            lookup_response = requests.post(
                "https://dev.khalti.com/api/v2/epayment/lookup/",
                headers={
                    "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "pidx": pidx
                },
                timeout=10
            )

        except requests.exceptions.RequestException:
            return Response(
                {"detail": "Unable to connect to Khalti. Please try again later."},
                status=status.HTTP_502_BAD_GATEWAY
            )

        # Parse Khalti response
        try:
            response_data = lookup_response.json()

        except requests.exceptions.JSONDecodeError:
            return Response(
                {"detail": "Khalti returned an invalid response."},
                status=status.HTTP_502_BAD_GATEWAY
            )

        payment_status = response_data.get("status")

        # Handle expired payment
        if lookup_response.status_code == 400 and payment_status == "Expired":
            payment.status = PaymentStatus.EXPIRED
            payment.save()

            return Response(
                {"detail": "Payment link has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Handle cancelled payment
        elif lookup_response.status_code == 400 and payment_status == "User canceled":
            payment.status = PaymentStatus.CANCELLED
            payment.save()

            return Response(
                {"detail": "Payment was cancelled by the user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Handle other HTTP errors
        if lookup_response.status_code != 200:
            return Response(
                {"detail": "Unable to verify payment with Khalti."},
                status=status.HTTP_502_BAD_GATEWAY
            )

        khalti_amount = response_data.get("total_amount")
        expected_amount = int(payment.total_amount * 100)

        # Handle successful payment

        if payment_status == "Completed" and khalti_amount == expected_amount:
         with transaction.atomic():
            payment.status = PaymentStatus.COMPLETED
            payment.save()

            payment.order.status = Status.PAID
            payment.order.save()

         return Response(
                {"detail": "Payment completed successfully."},
                status=status.HTTP_200_OK
            )

        # Handle amount mismatch
        elif payment_status == "Completed" and khalti_amount != expected_amount:
            payment.status = PaymentStatus.AMOUNT_MISMATCH
            payment.save()

            return Response(
                {"detail": "Payment amount mismatch. Please contact support."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Handle pending payment
        elif payment_status == "Pending":
            payment.status = PaymentStatus.PENDING
            payment.save()

            return Response(
                {"detail": "Payment is pending. Please wait for confirmation."},
                status=status.HTTP_200_OK
            )

        # Handle initiated payment
        elif payment_status == "Initiated":
            payment.status = PaymentStatus.INITIATED
            payment.save()

            return Response(
                {"detail": "Payment has been initiated. Awaiting confirmation."},
                status=status.HTTP_200_OK
            )

        # Handle failed payment
        elif payment_status == "Failed":
            payment.status = PaymentStatus.FAILED
            payment.save()

            return Response(
                {"detail": "Payment failed. Please try again."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Handle unexpected statuses
        else:
            return Response(
                {"detail": "Payment is not completed. Order remains pending."},
                status=status.HTTP_502_BAD_GATEWAY
            )
