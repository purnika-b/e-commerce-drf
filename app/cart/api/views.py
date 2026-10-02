from app.cart.models import CartItem
from app.cart.api.serializers import CartItemSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import IntegrityError
from django.shortcuts import get_object_or_404


@extend_schema("Read or get cart_item",
               tags=["Cart"]
            )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cart_view(request):
    cart_items=CartItem.objects.filter(user=request.user)
    serializer= CartItemSerializer(cart_items,many=True)
    return Response(serializer.data)


@extend_schema("create a cart item",request=CartItemSerializer, tags=["Cart"])
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cart_create(request):
 serializer = CartItemSerializer(data=request.data)
 if serializer.is_valid():
   try:
      serializer.save(user=request.user)
   except IntegrityError:
    return Response({"message":"Product is already in your cart."}, status=status.HTTP_400_BAD_REQUEST)
 return Response(serializer.data,status=status.HTTP_201_CREATED)

@extend_schema("Update the existing cart", tags=["Cart"])
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def cart_update(id,request):
  cart_item= get_object_or_404(CartItem,user=request.user,id=id)
  serializer=CartItemSerializer(cart_item,data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
  return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


@extend_schema("Delete an item", tags=(["Cart"]))
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def cart_delete(request,id):
  cart_item= get_object_or_404(CartItem,user=request.user,id=id)
  cart_item.delete()
  return Response({"message":"Cart item deleted successfully"},status=status.HTTP_200_OK)

