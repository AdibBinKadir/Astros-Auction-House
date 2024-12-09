from django.shortcuts import render
import datetime
from Products.models import Product
from django.http import HttpResponseRedirect, HttpResponse
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
    end_date = "Nov 30, 2024 23:26:00"



def home(request):
    return render(request, 'index.html', context={'date': date})  

def land(request):
    return HttpResponseRedirect('/landing/0')

def landing(request, index):
    products = Product.objects.all()
    if products.exists():
        if index >= len(products):
            index = len(products)-1
        if index < 0:
            index = 0
        brandname = products[index].brand_name
        productname = products[index].product_name
        startingprice = products[index].starting_price
        imgurl = products[index].image_url
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        if len(brandname) > 8:
            fs = 3
        else:
            fs = 6

        if 'Mobile' in user_agent:
            return render(request, 'mobile_landing.html', context={'date': date, 
                                                        'month': month, 
                                                        'day': day,
                                                        'products': products,
                                                        'fs': fs})
        elif 'Tablet' in user_agent or 'iPad' in user_agent:
            return render(request, 'mobile_landing.html', context={'date': date, 
                                                        'month': month, 
                                                        'day': day,  
                                                        'products': products,
                                                        'fs': fs})
        else:
            return render(request, 'landing.html', context={'date': date, 
                                                    'month': month, 
                                                    'day': day, 
                                                    'brandname': brandname, 
                                                    'productname': productname, 
                                                    'startingprice': startingprice, 
                                                    'imgurl': imgurl,
                                                    'index': index,
                                                    'fs': fs,})
    else:
        return HttpResponse("Sorry. We are out of products. Please come back later.")


