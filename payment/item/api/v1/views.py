from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, ListView
from item.models import Item
from shopping_cart.models import Order

# class ItemListView(ListView):
#     model = Item
#     template_name = "item_list.html"
#     context_object_name = "items"


@login_required
def item_list(request):
    object_list = Item.objects.all()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_products = [item.item for item in user_order_items]

    context = {"items": object_list, "current_order_products": current_order_products}

    return render(request, "item/item_list.html", context)


@method_decorator(csrf_protect, name="dispatch")
class ItemDetailView(DetailView):
    model = Item
    template_name = "item_detail.html"
    context_object_name = "item"
