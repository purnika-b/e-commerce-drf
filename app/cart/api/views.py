from app.cart.models import CartItem
from app.cart.api.serializers import CartItemSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated


@extend_schema("Read or get cart_item",
               tags=["Cart"]
            )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cart_view(request):
    cart_items=CartItem.objects.filter(user=request.user)
    serializer= CartItemSerializer(cart_items,many=True)
    return Response(serializer.data)
