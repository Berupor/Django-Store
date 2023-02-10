from django.urls import path

from .views import ItemDetailView, item_list

app_name = "item"

urlpatterns = [
    path("item/<int:pk>/", ItemDetailView.as_view(), name="item_detail"),
    path("item/", item_list, name="item_list"),
    # path("item/", ItemListView.as_view(), name="item_list"),
]
