from django.shortcuts import render, get_object_or_404
import stripe
from payment.models import Item
from django.http import JsonResponse
from django.views.generic import ListView, View, DetailView, TemplateView
from config.project_config import settings

stripe.api_key = settings.stripe.secret_key


class ItemListView(ListView):
    model = Item
    template_name = 'items_list.html'
    context_object_name = 'items'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'item_detail.html'
    context_object_name = 'item'
    pk_url_kwarg = 'id'


class ItemTemplateView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        item = Item.objects.get(id=1)
        context = super(ItemTemplateView).get_context_data(**kwargs)
        context.update({"STRIPE_PUBLIC_KEY": settings.stripe.public_key, "item ": item})
        return context


class CreateCheckoutSessionView(View):
    YOUR_DOMAIN = "http://127.0.0.1:8000"

    def post(self, request, *args, **kwargs):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': '{{PRICE_ID}}',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=self.YOUR_DOMAIN + '/success',
                cancel_url=self.YOUR_DOMAIN + '/cancel',
            )
        except Exception as e:
            return str(e)

        return JsonResponse({"id": checkout_session.id})


def buy_item(request, id):
    item = get_object_or_404(Item, id=id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'name': item.name,
            'description': item.description,
            'amount': int(item.price * 100),
            'currency': 'usd',
            'quantity': 1,
        }],
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
    )
    return render(request, 'buy_item.html', {'session_id': session.id})
    # return JsonResponse({"hi": "hi"})
