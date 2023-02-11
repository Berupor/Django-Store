from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Cents
    price = models.IntegerField(default=0)

    class Meta:
        db_table = "item"

    def __str__(self):
        return self.name

    def get_price(self):
        return round(self.price // 100)
