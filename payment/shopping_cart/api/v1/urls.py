from django.urls import path

from .views import add_to_cart, delete_from_cart, order_details

app_name = "shopping_cart"

urlpatterns = [
    path("cart/<int:item_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", order_details, name="order_summary"),
    path("cart/item/<str:item_id>/", delete_from_cart, name="delete_item"),
]
