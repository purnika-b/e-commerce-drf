from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from ..models import Product
from .serializers import ProductSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Products"],
    request=ProductSerializer
)
class ProductListCreateView(GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @extend_schema(summary="All products")
    def get(self, request):
        products = self.get_queryset()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

   
    
        
        

    @extend_schema(summary="Create products")
    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product created successfully"})

        return Response(serializer.errors)


@extend_schema(tags=["Products"])
class ProductDetailView(GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @extend_schema(summary="get one id")
    def get(self,request,id):
            product=get_object_or_404(Product,id=id)
            serializer=self.get_serializer(product)
            return Response(serializer.data)

    @extend_schema(summary="Update products")
    def put(self, request, id):
        product = get_object_or_404(Product, id=id)

        serializer = self.get_serializer(
            product,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product updated successfully"})

        return Response(serializer.errors)
        

    @extend_schema(summary="Update only what you want to change")
    def patch(self,request,id):
        product=get_object_or_404(Product,id=id)
        serializer=self.get_serializer(product,data=request.data,partial=True)
        if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "Product updated partially"})
            
        return Response(serializer.errors)



    @extend_schema(summary="Delete products")
    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)

        product.delete()

        return Response({"message": "Product deleted successfully"})