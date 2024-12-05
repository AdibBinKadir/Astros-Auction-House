from django.shortcuts import render
import datetime
from Products.models import Product
from django.http import HttpResponseRedirect
from Products.models import Product
import pytz


products = Product.objects.all()
if products.exists():
    earliest_product = products.order_by('startdt').first()
    latest_product = products.order_by('startdt').last()
    dtime_naive = earliest_product.startdt
    server_timezone = pytz.timezone('Asia/Dhaka')  # Replace with your server's timezone
    dtime = dtime_naive.astimezone(server_timezone)
    date = dtime.strftime('%b %d, %Y %H:%M:%S')
    month = dtime.strftime('%B')
    day = dtime.strftime('%d')
    end_date_naive = latest_product.startdt + datetime.timedelta(minutes=30)
    end_date = end_date_naive.astimezone(server_timezone)

else:
    date = "Nov 30, 2024 22:56:00"
    dtime = datetime.datetime.strptime(date, '%b %d, %Y %H:%M:%S')
    month = dtime.strftime('%B')
    day = dtime.strftime('%d')
    end_date = "Nov 30, 2024 23:26:00"



def home(request):
    return render(request, 'index.html', context={'date': date})  

def land(request):
    return HttpResponseRedirect('/landing/0')

def landing(request, index):
    products = Product.objects.all()
    if index >= len(products):
        index = len(products)-1
    if index < 0:
        index = 0
    brandname = products[index].brand_name
    productname = products[index].product_name
    startingprice = products[index].starting_price
    imgurl = products[index].image_url
    return render(request, 'landing.html', context={'date': date, 
                                                    'month': month, 
                                                    'day': day, 
                                                    'brandname': brandname, 
                                                    'productname': productname, 
                                                    'startingprice': startingprice, 
                                                    'imgurl': imgurl,
                                                    'index': index})

