from django.urls import include, path

urlpatterns = [
    path("v1/", include("profile.api.v1.urls")),
]
