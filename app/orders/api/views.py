from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from app.orders.models import Order,OrderItem, Status
from app.orders.api.serializers import OrderSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from app.cart.models import CartItem
from rest_framework import status
from django.db import transaction


class OrderCreateListView(GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes=[IsAuthenticated]

  
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    @extend_schema(
    summary="List customer orders",tags=["Order"]
)

    def get(self,request):
        orders=self.get_queryset()
        serializer=self.get_serializer(orders,many=True)
        return Response(serializer.data)
    
    @extend_schema(summary="Create the order",tags=["Order"])
    def post(self,request):
        cart_item=CartItem.objects.filter(user=request.user)

        if not cart_item.exists():
            return Response({"detail":"Your cart is empty."},status=status.HTTP_400_BAD_REQUEST,)
        for item in cart_item:
         if item.quantity>item.product.stock_quantity:
            return Response({"detail":"Insufficient stock available"},status=status.HTTP_400_BAD_REQUEST)
        total=0
        
        for item in cart_item:
            item.product.price*item.quantity
            total+=item.product.price*item.quantity

        with transaction.atomic():
         order=Order.objects.create(user=request.user,total_amount= total)
         for item in cart_item:
          item.product.stock_quantity=item.product.stock_quantity-item.quantity
          item.product.save()
          OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity, unit_price=item.product.price)
         cart_item.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Cancel a pending customer order",
        tags=["Order"],
    )
    def patch(self, request, *args, **kwargs):
        order = self.get_object()

        if order.status != Status.PENDING:
            return Response(
                {"detail": "Only pending orders can be cancelled"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = Status.CANCELLED
        order.save()

        serializer = self.get_serializer(order)
        return Response(serializer.data)
