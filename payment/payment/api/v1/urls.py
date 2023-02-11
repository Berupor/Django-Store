from django.urls import path

from .views import (BuyOrderView, CancelSuccessView,
                    SuccessTemplateView, stripe_webhook, update_transaction_records)

app_name = "payment"

urlpatterns = [
    path("webhook/stripe/", stripe_webhook, name="stripe_webhook"),
    path("buy/order/", BuyOrderView.as_view(), name="buy_order"),
    path("cancel/", CancelSuccessView.as_view(), name="cancel"),
    path("success/", SuccessTemplateView.as_view(), name="success"),
    path(
        "transaction/<str:token>/",
        update_transaction_records,
        name="update_records",
    ),
]
