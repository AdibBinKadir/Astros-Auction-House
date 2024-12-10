from django.db import models
import datetime

# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the product is being created (no primary key yet)
            if not Product.objects.exists():
                self.id = 1
            else:
                max_id = Product.objects.aggregate(models.Max('id'))['id__max']
                self.id = max_id + 1 if max_id else 1
        super().save(*args, **kwargs)
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
    winner = models.ForeignKey('Authenticate.UserProfile', on_delete=models.CASCADE, blank=True, null=True)
    highest_bid = models.IntegerField(default=models.F('starting_price'))
    brand_username = models.CharField(max_length=50, default="nowhere")
    startdt = models.DateTimeField(default=datetime.datetime.now)
    mailsent = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.id}: {self.product_name}"
    

class Bid(models.Model):
    user = models.ForeignKey('Authenticate.UserProfile', on_delete=models.CASCADE, db_column="user_id")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bid_amount = models.IntegerField()
    bid_time = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ['-bid_time']

    def __str__(self):
        return f"{self.user.fullname} bid {self.bid_amount}"
    
