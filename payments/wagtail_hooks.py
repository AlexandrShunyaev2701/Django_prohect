from wagtail.admin.panels import FieldPanel
from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from payments.models import Operation, Organization


class AdminPermissionHelper(PermissionHelper):
    """Custom permission helper for Operations model"""

    def user_can_delete_obj(self, user, obj) -> bool:
        """Method for checking delete permission for Operations model"""
        return False

    def user_can_edit_obj(self, user, obj) -> bool:
        """Method for checking edit permission for Operations model"""
        return False


class OrganizationAdmin(ModelAdmin):
    """Admin model for Organization."""

    model = Organization
    menu_label = "Organizations"
    menu_icon = "list-ol"
    list_display = ("id", "inn", "name", "address", "balance")
    panels = [
        FieldPanel("inn"),
        FieldPanel("name"),
        FieldPanel("address"),
        FieldPanel("balance"),
    ]


class OperationAdmin(ModelAdmin):
    """Admin model for Operation."""

    model = Operation
    menu_label = "Operations"
    menu_icon = "list-ol"
    list_display = (
        "operation_id",
        "amount",
        "organization",
        "document_number",
        "document_date",
        "created_at",
    )
    permission_helper_class = AdminPermissionHelper


modeladmin_register(OrganizationAdmin)
modeladmin_register(OperationAdmin)
