from django.urls import path
from .views import cart_view, cart_create, cart_update,cart_delete
urlpatterns=[
    path("cart-read/",cart_view,name="cart-read"),
    path("cart-create/", cart_create,name="cart-create"),
    path("cart-update/",cart_update,name="cart-update"),
    path("cart-delete/",cart_delete,name="cart-delete")
]