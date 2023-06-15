from typing import Any
from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=250)
    price = models.FloatField(default=0.0)
    brand = models.CharField(max_length=250,null=True,blank=True)
    rating = models.FloatField(default=0.0)
    category = models.CharField(max_length=250,null=True,blank=True)
    
    def save(self, *args, **kwargs):
        if self.category:
            self.category = self.category.replace("-", "_").replace(" ", "_")
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.title)

