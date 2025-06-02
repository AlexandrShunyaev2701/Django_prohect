from rest_framework import serializers

from payments.models import Organization


class PaymentWebhookSerializer(serializers.Serializer):
    """Serializer for Payments."""

    operation_id = serializers.UUIDField()
    amount = serializers.IntegerField()
    payer_inn = serializers.CharField(max_length=100)
    document_number = serializers.CharField(max_length=64)
    document_date = serializers.DateTimeField()


class OrganizationBalanceSerializer(serializers.ModelSerializer):
    """Serializer for Organization."""

    class Meta:
        model = Organization
        fields = ("inn", "balance")


class WebhookImitationParamsSerializer(serializers.Serializer):
    """Serializer for WebhookImitation."""

    operation_id = serializers.UUIDField(required=False)
    amount = serializers.IntegerField(required=False)
    payer_inn = serializers.CharField(required=False, max_length=100)
    document_number = serializers.CharField(required=False, max_length=64)
    document_date = serializers.DateTimeField(required=False)
