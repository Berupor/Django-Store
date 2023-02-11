from django.db import models

from item.models import Item
from profile.models import Profile


class OrderItem(models.Model):
    item = models.OneToOneField(Item, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    class Meta:
        db_table = "order_item"

    def __str__(self):
        return self.item.name


class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "order"

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.item.get_price() for item in self.items.all()])

    def get_cart_total_cents(self):
        return sum([item.item.price for item in self.items.all()])

    def __str__(self):
        return f"{self.owner.user} - {self.ref_code}"
