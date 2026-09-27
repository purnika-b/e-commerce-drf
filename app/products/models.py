from django.db import models

# Create your models here.
class Category(models.Model):
    
    name=models.CharField(max_length=20,unique=True)
    description=models.TextField(max_length=1000)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
            return self.name

class Product(models.Model):
    name=models.CharField(max_length=50)
    brand= models.CharField(max_length=50)
    type=models.CharField(max_length=50)
    description=models.TextField(max_length=500)
    price=models.DecimalField(max_digits=8, decimal_places=2)
    stock_quantity=models.IntegerField()

    category=models.ForeignKey(Category,on_delete=models.PROTECT)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to="products/", blank=True, null=True)