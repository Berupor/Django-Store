from django.shortcuts import render

from profile.models import Profile
from shopping_cart.models import Order


def profile(request):
    user_profile = Profile.objects.filter(user=request.user).first()
    orders = Order.objects.filter(is_ordered=True, owner=user_profile)
    context = {"orders": orders}

    return render(request, "profile/profile.html", context)
