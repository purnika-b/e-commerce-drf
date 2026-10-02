from django.contrib import admin
from .models import CartItem
admin.site.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity"]
    search_fields = ["user__username", "product__name"]
    list_filter = ["product"]

# Register your models here.
