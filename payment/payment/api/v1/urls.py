from django.urls import path

from .views import (BuyOrderView, CancelSuccessView, CreateCheckoutSessionView,
                    SuccessTemplateView, stripe_webhook)

app_name = "payment"

urlpatterns = [
    path("webhook/stripe/", stripe_webhook, name="stripe_webhook"),
    # path("item/<int:pk>/", ItemDetailView.as_view(), name="item_detail"),
    # path("items/", ItemListView.as_view(), name="item_list"),
    path("buy/item/<int:pk>", CreateCheckoutSessionView.as_view(), name="buy_item"),
    path("buy/order/", BuyOrderView.as_view(), name="buy_order"),
    path("cancel/", CancelSuccessView.as_view(), name="cancel"),
    path("success/", SuccessTemplateView.as_view(), name="success"),
]
