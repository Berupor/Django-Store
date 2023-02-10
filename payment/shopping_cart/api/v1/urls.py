from django.urls import path

from .views import (add_to_cart, checkout, delete_from_cart,  # success
                    order_details, update_transaction_records)

app_name = "shopping_cart"

urlpatterns = [
    path("cart/<int:item_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", order_details, name="order_summary"),
    # path('success/', success, name='purchase_success'),
    path("cart/item/<str:item_id>/", delete_from_cart, name="delete_item"),
    path("checkout/", checkout, name="checkout"),
    path(
        "update-transaction/<str:token>/",
        update_transaction_records,
        name="update_records",
    ),
]
