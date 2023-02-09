from django.urls import path
from .views import buy_item, ItemListView, ItemDetailView, ItemTemplateView

urlpatterns = [
    # path('item/<int:id>/', item_detail, name='item_detail'),
    path('item/<int:id>/', ItemDetailView.as_view(), name='item_detail'),
    path('buy/<int:id>/', buy_item, name='buy_item'),
    path('items/', ItemListView.as_view(), name='item_list'),
    path('landing/', ItemTemplateView.as_view(), name='landing'),
    path('create_checkout_session', )

]
