from django.db import models

class PaymentStatus(models.TextChoices):
      PENDING="pending","Pending"
      COMPLETED="completed","Completed"
      FAILED="failed","Failed"
      EXPIRED="expired","Expired"
      CANCELLED="cancelled","Cancelled"
      AMOUNT_MISMATCH = "amount_mismatch", "Amount mismatch"
      INITIATED="initiated","Initiated"
      
# Create your models here.
class Payment(models.Model):
      order=models.ForeignKey("orders.Order",on_delete=models.PROTECT,related_name="payments",)
      total_amount=models.DecimalField(max_digits=12,decimal_places=2)
      pidx=models.CharField(max_length=100,unique=True,null=True,blank=True,)
      status=models.CharField(max_length=20,choices=PaymentStatus.choices,default=PaymentStatus.PENDING)
      created_at=models.DateTimeField(auto_now_add=True)
      updated_at=models.DateTimeField(auto_now=True)

