from django.db import models

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255)
    starting_price = models.IntegerField()
    image_url = models.CharField(max_length=2083)
    image_url2 = models.CharField(max_length=2083, blank=True, null=True)
    image_url3 = models.CharField(max_length=2083, blank=True, null=True)
    image_url4 = models.CharField(max_length=2083, blank=True, null=True)
    image_url5 = models.CharField(max_length=2083, blank=True, null=True)
    product_description = models.TextField(default="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent a nisl ex. Suspendisse ut orci tort")
    product_dimensions = models.TextField(default="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent a nisl ex. Suspendisse ut orci tort")
    winner = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    highest_bid = models.IntegerField(default=0)
    brand_username = models.CharField(max_length=50, default="nowhere")

    def __str__(self):
        return f"{self.id}: {self.product_name}"
    

class Bid(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bid_amount = models.FloatField()

    def __str__(self):
        return f"{self.user} bid {self.bid_amount} on {self.product}"
    
