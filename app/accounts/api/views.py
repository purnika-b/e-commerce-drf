from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import RegisterSerializer, ProfileSerializer
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView

@extend_schema(tags=["Accounts"])
class LoginView(TokenObtainPairView):
   pass

@extend_schema(
   request=RegisterSerializer,
   tags=["Accounts"]
)
class RegisterView(GenericAPIView):
    serializer_class=RegisterSerializer

    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
         serializer.save()
         return Response({"message":"User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
   tags=["Accounts"]
)  
class ProfileView(RetrieveUpdateAPIView):
   serializer_class= ProfileSerializer
   permission_classes = [IsAuthenticated]

   def get_object(self):
      return self.request.user  

    