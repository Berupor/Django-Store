from django.urls import include, path

urlpatterns = [
    path("v1/", include("item.api.v1.urls")),
]
