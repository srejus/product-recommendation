from django.db import models
from django.contrib.auth.models import User

from product.models import Product

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ordered_by')
    ordered_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField(default=0.0)
    rating = models.FloatField(default=0.0)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_item')
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,related_name='product_name')
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=1)
