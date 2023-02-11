from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from item.models import Item
from profile.models import Profile
from shopping_cart.extras import generate_order_id
from shopping_cart.models import Order, OrderItem


def get_user_pending_order(request):
    profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=profile, is_ordered=False)
    if order.exists():
        return order[0]
    return 0


@login_required()
def add_to_cart(request, item_id):
    profile = get_object_or_404(Profile, user=request.user)
    item = get_object_or_404(Item, id=item_id)
    if item in profile.items.all():
        return redirect("item:item_list")

    order_item, created = OrderItem.objects.get_or_create(item=item)
    user_order, created = Order.objects.get_or_create(owner=profile, is_ordered=False)

    user_order.items.add(order_item)
    if created:
        user_order.ref_code = generate_order_id()
        user_order.save()

    return redirect("item:item_list")


@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = get_object_or_404(OrderItem, id=item_id)
    item_to_delete.delete()
    return redirect("shopping_cart:order_summary")


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {"order": existing_order}
    return render(request, "shopping_cart/order_summary.html", context)
