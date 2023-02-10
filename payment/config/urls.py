from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("payment.api.urls")),
    path("api/", include("item.api.urls")),
    path("api/", include("profile.api.urls")),
    path("api/", include("shopping_cart.api.urls")),
]
