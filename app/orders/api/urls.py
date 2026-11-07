from django.urls import path
from app.orders.api.views import OrderCreateListView, OrderDetailView

urlpatterns=[
    path("",OrderCreateListView.as_view(),name="order-list"),
    path("<int:pk>/",OrderDetailView.as_view(),name="order-update"),
]
