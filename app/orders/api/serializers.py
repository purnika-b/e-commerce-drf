from rest_framework import serializers
from app.orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        field=["id", "product", "quantity", "unit_price"]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields = [
            "id",
            "user",
            "items",
            "total_amount",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "total_amount",
            "status",
            "created_at",
            "updated_at",
        ]