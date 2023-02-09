import stripe
from config.project_config import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, View, DetailView, TemplateView
from payment.models import Item

stripe.api_key = settings.stripe.secret_key


class SuccessTemplateView(TemplateView):
    template_name = 'success.html'


class CancelSuccessView(TemplateView):
    template_name = 'cancel.html'


class ItemListView(ListView):
    model = Item
    template_name = 'items_list.html'
    context_object_name = 'items'


@method_decorator(csrf_protect, name='dispatch')
class ItemDetailView(DetailView):
    model = Item
    template_name = 'item_detail.html'
    context_object_name = 'item'


class CreateCheckoutSessionView(View):
    YOUR_DOMAIN = "http://127.0.0.1:8000/api/v1"

    def post(self, request, *args, **kwargs):
        item = get_object_or_404(Item, id=kwargs.get('pk'))

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price_data': {
                            'unit_amount': item.price,
                            'currency': 'usd',
                            'product_data': {
                                'name': item.name,

                            }
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=self.YOUR_DOMAIN + '/success/',
                cancel_url=self.YOUR_DOMAIN + '/cancel/',
            )
        except Exception as e:
            print(e)
            return JsonResponse({"success": "false"})

        return redirect(checkout_session.url, code=303)
