from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from item.models import Item
from shopping_cart.models import Order


class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = "item/item_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_orders = Order.objects.filter(owner=self.request.user.profile, is_ordered=False)
        current_order_products = []
        if filtered_orders.exists():
            user_order = filtered_orders[0]
            user_order_items = user_order.items.all()
            current_order_products = [item.item for item in user_order_items]
        context["current_order_products"] = current_order_products
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = "item/item_detail.html"
    context_object_name = "item"
