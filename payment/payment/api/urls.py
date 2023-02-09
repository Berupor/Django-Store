from django.urls import include, path

urlpatterns = [
    path("v1/", include("payment.api.v1.urls")),
]