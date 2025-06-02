from decimal import Decimal

from celery import shared_task
from django.db import transaction

from commons.loggers import logger


@shared_task
def create_payment_update_balance(data: dict) -> None:
    """Task for create payment and update balance for organization."""
    from payments.models import Operation, Organization

    try:
        with transaction.atomic():
            org = Organization.objects.select_for_update().get(
                inn=data.get("payer_inn")
            )

            amount = Decimal(data.get("amount"))
            org.balance += amount
            org.save(update_fields=["balance"])

            payment = Operation.objects.create(
                operation_id=data.get("operation_id"),
                amount=amount,
                document_number=data.get("document_number"),
                document_date=data.get("document_date"),
                organization=org,
            )

            logger.info(
                f"New operation {payment.operation_id} created. "
                f"Organization with inn: {org.inn}, new balance: {org.balance}"
            )

    except Organization.DoesNotExist:
        logger.error(f"Organization with inn {data.get('payer_inn')} does not exist")
    except Exception as e:
        logger.error(f"Error processing the webhook from the bank: {e}")
