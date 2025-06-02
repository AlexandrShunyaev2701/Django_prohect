import uuid
from datetime import datetime, timezone

import requests
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from commons.loggers import logger
from payments.models import Operation, Organization
from payments.serializers import (
    PaymentWebhookSerializer,
    WebhookImitationParamsSerializer,
)
from payments.services import cache_service
from payments.tasks import create_payment_update_balance


class BankWebhookView(APIView):
    """View for webhook from the Bank API."""

    def post(self, request: Request) -> Response:
        """POST from Bank API."""
        serializer = PaymentWebhookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if Operation.objects.filter(operation_id=data.get("operation_id")).exists():
            logger.info(
                f"Duplicate operation with operation_id: {data.get('operation_id')}. Ignored"
            )
            return Response(
                {"detail": "Duplicate operation. Ignored."}, status=status.HTTP_200_OK
            )

        create_payment_update_balance.delay(data)

        return Response({"status": "success"}, status=status.HTTP_200_OK)


class OrganizationBalanceView(APIView):
    """
    GET /api/organizations/<inn>/balance/
    """

    def get(self, request: Request, inn: str) -> Response:
        """Get inn and balance organizations"""
        data = cache_service.get_organization_info(inn)
        if not data:
            organization = Organization.objects.filter(inn=inn).first()
            if not organization:
                return Response(
                    {"detail": "Organization not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            data = cache_service.refresh_cache(organization, inn)
        return Response(data)


class BankWebhookImitatorView(APIView):
    """Imitation view"""

    @swagger_auto_schema(
        request_body=WebhookImitationParamsSerializer,
        responses={200: openapi.Response("Webhook imitation result")},
    )
    def post(self, request: Request) -> Response:
        """Post to Imitation view"""
        params_serializer = WebhookImitationParamsSerializer(data=request.data)
        params_serializer.is_valid(raise_exception=True)
        params = params_serializer.validated_data

        data = {
            "operation_id": str(params.get("operation_id", uuid.uuid4())),
            "amount": params.get("amount", 145000),
            "payer_inn": params.get("payer_inn", "1234567890"),
            "document_number": params.get("document_number", "PAY-328"),
            "document_date": (
                params.get("document_date").isoformat()
                if params.get("document_date")
                else datetime.now(timezone.utc).isoformat()
            ),
        }

        webhook_url = request.build_absolute_uri(reverse("bank-webhook"))

        response = requests.post(webhook_url, json=data)

        return Response(
            {
                "sent_data": data,
                "webhook_url": webhook_url,
                "bank_webhook_status_code": response.status_code,
                "bank_webhook_response": response.json() if response.content else None,
            },
            status=status.HTTP_200_OK,
        )
