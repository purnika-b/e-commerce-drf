from django.urls import path
from .views import cart_view
urlpatterns=[
    path("cart-read/",cart_view,name="cart-read")
]