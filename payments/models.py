import uuid

from django.db import models

from payments.services import cache_service


class Organization(models.Model):
    """Model representing an organization."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inn = models.CharField("INN organizations", max_length=100, unique=True)
    name = models.CharField("Organization name", max_length=100, blank=True, null=True)
    address = models.CharField(
        "Organization address", max_length=100, blank=True, null=True
    )
    balance = models.DecimalField("Balance", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def save(self, *args, **kwargs) -> None:
        """Save method with create and update cache"""
        super().save(*args, **kwargs)
        cache_service.refresh_cache(self, self.inn)

    def delete(self, *args, **kwargs) -> None:
        """Delete method with create and update cache"""
        cache_service.clear_cache(self.inn)
        super().delete(*args, **kwargs)

    def __str__(self):
        """Return inn and balance"""
        return f"Organization with inn: {self.inn}, balance: {self.balance}"


class Operation(models.Model):
    """Model representing a operation."""

    operation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Operation ID",
    )
    amount = models.DecimalField("Amount", max_digits=10, decimal_places=2)
    organization = models.ForeignKey(
        Organization, on_delete=models.PROTECT, verbose_name="Organization"
    )
    document_number = models.CharField("Document number", max_length=64)
    document_date = models.DateField("Document date")
    created_at = models.DateTimeField("Create date", auto_now_add=True)

    def __str__(self):
        """Return id and status operation"""
        return f"Operation ID: {self.operation_id} - status: {self.status}"

    class Meta:
        verbose_name = "Operation"
        verbose_name_plural = "Operations"
