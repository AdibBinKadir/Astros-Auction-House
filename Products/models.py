from django.db import models

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255)
    starting_price = models.FloatField()
    image_url = models.CharField(max_length=2083)

    def __str__(self):
        return f"{self.id}: {self.product_name}"
    
