from django.urls import path

from .views import ItemDetailView, ItemListView

app_name = "item"

urlpatterns = [
    path("items/<int:pk>/", ItemDetailView.as_view(), name="item_detail"),
    path("items/", ItemListView.as_view(), name="item_list"),
]
