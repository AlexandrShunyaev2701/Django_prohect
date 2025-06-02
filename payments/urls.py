from django.urls import path
from .views import (
    BankWebhookView,
    OrganizationBalanceView,
    BankWebhookImitatorView,
)

urlpatterns = [
    path('webhook/bank/', BankWebhookView.as_view(), name='bank-webhook'),
    path('organizations/<str:inn>/balance/', OrganizationBalanceView.as_view(), name='organization-balance'),
    path('webhook/bank/imitation/', BankWebhookImitatorView.as_view(), name='bank-webhook-imitation'),
]
