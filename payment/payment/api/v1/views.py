import datetime
from profile.models import Profile

import stripe
from config.project_config import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View
from item.models import Item
from shopping_cart.api.v1.views import get_user_pending_order
from shopping_cart.models import Transaction

stripe.api_key = settings.stripe.secret_key


class SuccessTemplateView(TemplateView):
    template_name = "success.html"


class CancelSuccessView(TemplateView):
    template_name = "cancel.html"


class CreateCheckoutSessionView(View):
    YOUR_DOMAIN = "http://127.0.0.1:8000/api/v1"

    def post(self, request, *args, **kwargs):
        item = get_object_or_404(Item, id=kwargs.get("pk"))

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "unit_amount": item.price,
                            "currency": "usd",
                            "product_data": {
                                "name": item.name,
                            },
                        },
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url=self.YOUR_DOMAIN + "/success/",
                cancel_url=self.YOUR_DOMAIN + "/cancel/",
            )
        except Exception as e:
            print(e)
            return JsonResponse({"success": "false"})

        return redirect(checkout_session.url, code=303)


class BuyOrderView(View):
    YOUR_DOMAIN = "http://127.0.0.1:8000/api/v1"

    def post(self, request, *args, **kwargs):
        existing_order = get_user_pending_order(request)

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "unit_amount": existing_order.get_cart_total(),
                            "currency": "usd",
                            "product_data": {
                                "name": f"Order: {existing_order.ref_code}",
                            },
                        },
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url=self.YOUR_DOMAIN + "/success/",
                cancel_url=self.YOUR_DOMAIN + "/cancel/",
            )
        except Exception as e:
            print(e)
            return JsonResponse({"success": "false"})

        return redirect(checkout_session.url, code=303)


@login_required()
def update_transaction_records(request, token):
    # get the order being processed
    order_to_purchase = get_user_pending_order(request)

    # update the placed order
    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered = datetime.datetime.now()
    order_to_purchase.save()

    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Add products to user profile
    profile = get_object_or_404(Profile, user=request.user)
    # get the products from the items
    order_products = [item.item for item in order_items]
    profile.items.add(*order_products)
    profile.save()

    # create a transaction
    transaction = Transaction(
        profile=request.user.profile,
        token=token,
        order_id=order_to_purchase.id,
        amount=order_to_purchase.get_cart_total(),
        success=True,
    )
    # save the transcation (otherwise doesn't exist)
    transaction.save()

    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    # messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse("accounts:my_profile"))


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe.webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == "payment_intent.succeeded":
        payment_intent = event.data.object  # contains a stripe.PaymentIntent
        print(event)
        print("PaymentIntent was successful!")
    elif event.type == "payment_method.attached":
        payment_method = event.data.object  # contains a stripe.PaymentMethod
        print("PaymentMethod was attached to a Customer!")
    # ... handle other event types
    else:
        print("Unhandled event type {}".format(event.type))

    return HttpResponse(status=200)
