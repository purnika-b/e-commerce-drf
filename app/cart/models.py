from django.db import models
from app.products.models import Product
from django.conf import settings


# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity=models.IntegerField()

    class Meta:
      constraints=[
        models.UniqueConstraint(
            fields=["user","product"],
            name="unique_user_product"


        )
    ]
