from rest_framework import serializers
from app.cart.models import CartItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=["product","quantity"]
        