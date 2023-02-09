from django.urls import path
from .views import ItemListView, ItemDetailView, CreateCheckoutSessionView, CancelSuccessView, SuccessTemplateView

urlpatterns = [
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('items/', ItemListView.as_view(), name='item_list'),
    path('buy/<int:pk>', CreateCheckoutSessionView.as_view(), name='buy'),
    path('cancel/', CancelSuccessView.as_view(), name='cancel'),
    path('success/', SuccessTemplateView.as_view(), name='success'),

]
