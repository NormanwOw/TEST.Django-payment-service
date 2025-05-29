from django.urls import path

from payment.presentation.views import BankWebhookView, OrganizationBalanceView

app_name = 'payment'

urlpatterns = [
    path('api/webhook/bank/',
         BankWebhookView.as_view(),
         name='bank-webhook'),
    path('api/organizations/<int:inn>/balance/',
         OrganizationBalanceView.as_view(),
         name='organization-balance'),
]
