from django.urls import include, path

urlpatterns = [
    path("v1/", include("shopping_cart.api.v1.urls")),
]
