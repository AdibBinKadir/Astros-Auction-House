from django.shortcuts import render
import datetime
from Products.models import Product
from django.http import HttpResponseRedirect

date = "Dec 31, 2024 16:17:00"
dtime = datetime.datetime.strptime(date, '%b %d, %Y %H:%M:%S')
month = dtime.strftime('%B')
day = dtime.strftime('%d')


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

