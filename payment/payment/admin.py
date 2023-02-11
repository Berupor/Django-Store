from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["profile", "order_id", "amount", "success", "timestamp"]
    list_filter = ["success", "timestamp"]
    search_fields = ["order_id", "token"]
