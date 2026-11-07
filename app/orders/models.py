from django.db import models
from django.conf import settings
from app.products.models import Product

class Status(models.TextChoices):
    PENDING="pending","Pending"
    PAID="paid","Paid"
    SHIPPED="shipped","Shipped"
    DELIVERED="delivered","Delivered"
    CANCELLED="cancelled","Cancelled"

# Create your models here.
class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="orders",)
    total_amount=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING,)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order= models.ForeignKey(Order,on_delete=models.PROTECT,  related_name="items",)
    product=models.ForeignKey(Product, on_delete=models.PROTECT,)
    quantity=models.PositiveIntegerField(default=1)
    unit_price=models.DecimalField(max_digits=12,decimal_places=2,)


