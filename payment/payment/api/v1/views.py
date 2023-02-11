from profile.models import Profile
import uuid

import stripe
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View

from config.project_config import settings
from payment.models import Transaction
from profile.models import Profile
from shopping_cart.api.v1.views import get_user_pending_order
from shopping_cart.models import Order

stripe.api_key = settings.stripe.secret_key


class SuccessTemplateView(TemplateView):
    template_name = "success.html"


class CancelSuccessView(TemplateView):
    template_name = "cancel.html"


class BuyOrderView(View):
    YOUR_DOMAIN = "http://localhost:8000/api/v1"

    def post(self, request, *args, **kwargs):
        existing_order = get_user_pending_order(request)
        # Generate a unique token for the transaction
        token = uuid.uuid4().hex

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "unit_amount": existing_order.get_cart_total_cents(),
                            "currency": "usd",
                            "product_data": {
                                "name": f"Order: {existing_order.ref_code}",
                            },
                        },
                        "quantity": 1,

                    },
                ],
                payment_intent_data={
                    "metadata": {
                        "user_id": request.user.id,
                        "order_id": existing_order.id,
                        "token": token,
                    }
                },
                mode="payment",
                success_url=self.YOUR_DOMAIN + "/success/",
                cancel_url=self.YOUR_DOMAIN + "/cancel/",
            )

        except Exception as e:
            return JsonResponse({"Error": e.args[0]})

        return redirect(checkout_session.url, code=303)


def update_transaction_records(token, user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)
    order_to_purchase = Order.objects.get(owner=profile, is_ordered=False)

    # update the placed order
    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered = timezone.now()
    order_to_purchase.save()

    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=timezone.now())

    # Add products to user profile
    # get the products from the items
    order_products = [item.item for item in order_items]
    profile.items.add(*order_products)
    profile.save()

    # create a transaction
    transaction = Transaction(
        profile=profile,
        token=token,
        order_id=order_to_purchase.id,
        amount=order_to_purchase.get_cart_total(),
        success=True,
    )
    # save the transcation (otherwise doesn't exist)
    transaction.save()


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
        session = event['data']['object']

        user_id = session['metadata']['user_id']
        token = session['metadata']['token']

        update_transaction_records(user_id=user_id, token=token, )
    elif event.type == "payment_method.attached":
        payment_method = event.data.object  # contains a stripe.PaymentMethod
    else:
        print("Unhandled event type {}".format(event.type))
    return HttpResponse(status=200)
