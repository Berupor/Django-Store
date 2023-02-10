import datetime
from profile.models import Profile

from config.project_config import settings
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from item.models import Item
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
        messages.info(request, "You already own this item")
        return redirect("item:item_list")

    order_item, created = OrderItem.objects.get_or_create(item=item)
    print(created)

    user_order, created = Order.objects.get_or_create(owner=profile, is_ordered=False)
    print(created)

    user_order.items.add(order_item)
    if created:
        user_order.ref_code = generate_order_id()
        user_order.save()

    messages.info(request, "Item added to cart")
    return redirect("item:item_list")


@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")

    return redirect(reverse("shopping_cart:order_summary"))


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {"order": existing_order}
    return render(request, "shopping_cart/order_summary.html", context)


@login_required()
def checkout(request):
    existing_order = get_user_pending_order(request)
    context = {"order": existing_order}
    return render(request, "checkout.html", context)


@login_required()
def process_payment(request, order_id):
    return redirect(
        reverse("shopping_cart:update_records", kwargs={"order_id": order_id})
    )


@login_required()
def update_transaction_records(request, order_id):
    order_to_purchase = Order.objects.filter(pk=order_id).first()

    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered = datetime.datetime.now()
    order_to_purchase.save()

    order_items = order_to_purchase.items.all()

    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    profile = get_object_or_404(Profile, user=request.user)

    order_items = [item.product for item in order_items]
    profile.items.add(*order_items)
    profile.save()

    messages.info(request, "Your items have been added to your cart.")
    return redirect(reverse("accounts:my_profile"))
