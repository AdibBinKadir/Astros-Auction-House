from django.shortcuts import render
from .models import Product, Bid
from Authenticate.models import UserProfile
from django.utils import timezone

import datetime
from django.http import HttpResponseRedirect, JsonResponse
import pytz

remaining = -5000
# Create your views here.


def prod_red(request, index):
    return HttpResponseRedirect(f'/products/{index}/1')

def products(request, index, scr):
    products = Product.objects.all()
    brandname = products[index].brand_name
    desc = products[index].product_description
    url1 = products[index].image_url
    url2 = products[index].image_url2
    url3 = products[index].image_url3
    url4 = products[index].image_url4
    url5 = products[index].image_url5
    urls = [url1, url2, url3, url4, url5]
    brand_username = products[index].brand_username
    if products[index].winner:
        winner_name = products[index].winner.fullname
    else:
        winner_name = None
    dimensions = products[index].product_dimensions
    highest_bid = products[index].highest_bid
    urls = [url for url in urls if url is not None]

    
    
    start = products[index].starting_price
    highest = max(start, highest_bid)

    user_agent = request.META.get('HTTP_USER_AGENT', '')

    if 'Mobile' in user_agent:
        template = 'mobile_prod.html'
    elif 'Tablet' in user_agent or 'iPad' in user_agent:
        template = 'mobile_prod.html'
    else:
        template = 'product.html'

    server_timezone = pytz.timezone('Asia/Dhaka')  # Replace with your server's timezone
    startdt_aware = products[index].startdt.astimezone(server_timezone)
    hour = startdt_aware.strftime('%H')
    if int(hour) > 12:
        hour = str(int(hour) - 12)
        md = 'PM'
    else:
        md = 'AM'
    minute = startdt_aware.strftime('%M')

    end_date = startdt_aware + datetime.timedelta(minutes=30)
    enddt_aware = end_date.astimezone(server_timezone)
    
    curr_date = datetime.datetime.now(datetime.timezone.utc)
    currdt_aware = curr_date.astimezone(server_timezone)

    if request.user.is_authenticated:
        user = UserProfile.objects.get(user=request.user)
        verified = user.verified
        if products[index].winner == user:
            W = True
        else:
            W = False
    else:
        user = None
        verified = False
        W = False


    if (request.user.is_authenticated) and (enddt_aware > currdt_aware > startdt_aware) and (verified):
        auctionable = 1
    elif (enddt_aware < currdt_aware):
        auctionable = -1
    else:
        auctionable = 0


    

    bids = Bid.objects.filter(product=products[index])

    bids = [str(bid) for bid in bids]

    if len(brand_username) > 8:
        fs = 8
    else:
        fs = 12.5


    context = {
        'desc': desc,
        'urls': urls,
        'highest': highest,
        'brandname': brandname,
        'dimensions': dimensions,
        'index': index,
        'auctionable': auctionable,
        'bids': bids,
        'end_date': enddt_aware.strftime('%b %d, %Y %H:%M:%S'),
        'scr': scr,
        'winner': winner_name,
        'remaining': remaining,
        'brand_username': brand_username,
        'verified': verified,
        'W': W,
        'fs': fs,
        'hour': hour,
        'minute': minute,
        'md': md,

    }

    return render(request, template, context)


def left_prod(request, index):
    products = Product.objects.all()
    brandname = products[index].brand_name
    desc = products[index].product_description
    url1 = products[index].image_url
    url2 = products[index].image_url2
    url3 = products[index].image_url3
    url4 = products[index].image_url4
    url5 = products[index].image_url5
    urls = [url1, url2, url3, url4, url5]
    dimensions = products[index].product_dimensions
    highest_bid = products[index].highest_bid
    urls = [url for url in urls if url is not None]
    brand_username = products[index].brand_username

    start = products[index].starting_price
    highest = max(start, highest_bid)
    context = {
        'desc': desc,
        'urls': urls,
        'highest': highest,
        'brandname': brandname,
        'dimensions': dimensions,
        'index': index,
        'brand_username': brand_username,
    }

    return render(request, 'left.html', context)


def right_prod(request, index):
    products = Product.objects.all()
    brandname = products[index].brand_name
    desc = products[index].product_description
    url1 = products[index].image_url
    url2 = products[index].image_url2
    url3 = products[index].image_url3
    url4 = products[index].image_url4
    url5 = products[index].image_url5
    urls = [url1, url2, url3, url4, url5]
    dimensions = products[index].product_dimensions
    highest_bid = products[index].highest_bid
    urls = [url for url in urls if url is not None]

    if products[index].winner:
        winner_name = products[index].winner.fullname
    else:
        winner_name = None

    start = products[index].starting_price
    highest = max(start, highest_bid)
    server_timezone = pytz.timezone('Asia/Dhaka')  # Replace with your server's timezone
    startdt_aware = products[index].startdt.astimezone(server_timezone)

    hour = startdt_aware.strftime('%H')
    if int(hour) > 12:
        hour = str(int(hour) - 12)
        md = 'PM'
    else:
        md = 'AM'
    minute = startdt_aware.strftime('%M')

    end_date = startdt_aware + datetime.timedelta(minutes=30)
    enddt_aware = end_date.astimezone(server_timezone)
    
    curr_date = datetime.datetime.now(datetime.timezone.utc)
    currdt_aware = curr_date.astimezone(server_timezone)

    if request.user.is_authenticated:
        user = UserProfile.objects.get(user=request.user)
        verified = user.verified
        if products[index].winner == user:
            W = True
        else:
            W = False
    else:
        user = None
        verified = False
        W = False
    if (request.user.is_authenticated) and (enddt_aware > currdt_aware > startdt_aware) and (verified):
        auctionable = 1
    elif (enddt_aware < currdt_aware):
        auctionable = -1
    else:
        auctionable = 0
    


    bids = Bid.objects.filter(product=products[index])
    bids = [str(bid) for bid in bids]
    context = {
        'desc': desc,
        'urls': urls,
        'highest': highest,
        'brandname': brandname,
        'dimensions': dimensions,
        'index': index,
        'bids': bids,
        'auctionable': auctionable,
        'end_date': end_date.strftime('%b %d, %Y %H:%M:%S'),
        'winner': winner_name,
        'remaining': remaining,
        'verified': verified,
        'W': W,
        'hour': hour,
        'minute': minute,
        'md': md,
    }


    return render(request, 'right.html', context)


def bid(request, index, amount):
    global remaining
    products = Product.objects.all()
    user = UserProfile.objects.get(user=request.user)
    verified = user.verified
    cooldown = user.cooldown
    curr_date = datetime.datetime.now(datetime.timezone.utc)
    currdt_aware = curr_date.astimezone(pytz.timezone('Asia/Dhaka'))
    if Bid.objects.filter(user=user, product=products[index]).exists():
        last_bid = Bid.objects.filter(user=user, product=products[index])[0]
        lb_time = last_bid.bid_time
        lb_time_aware = lb_time.astimezone(pytz.timezone('Asia/Dhaka'))
        
        remaining = user.cooldown - int((currdt_aware - lb_time_aware).seconds)
        if remaining > 0:
            pass
        else:
            product = products[index]
            user = UserProfile.objects.get(user=request.user)
            product.highest_bid = (products[index].highest_bid + amount)
            product.winner = user
            product.save()
            if Bid.objects.filter(product=product, user=user).exists():
                Bid.objects.filter(product=product, user=user).delete()
            bid = Bid.objects.create(
                user=user,
                product=product,
                bid_amount= (products[index].highest_bid),
                bid_time=currdt_aware
            )
            bid.save()
    else:
        product = products[index]
        user = UserProfile.objects.get(user=request.user)
        product.highest_bid = (products[index].highest_bid + amount)
        product.winner = user
        product.save()
        if Bid.objects.filter(product=product, user=user).exists():
            Bid.objects.filter(product=product, user=user).delete()
        bid = Bid.objects.create(
            user=user,
            product=product,
            bid_amount= (products[index].highest_bid),
            bid_time=currdt_aware
        )
        bid.save()



    user_agent = request.META.get('HTTP_USER_AGENT', '')

    if 'Mobile' in user_agent:
        return HttpResponseRedirect(f'/products/{index}/2')
    elif 'Tablet' in user_agent or 'iPad' in user_agent:
        return HttpResponseRedirect(f'/products/{index}/2')
    else:
        return HttpResponseRedirect(f'/products/right/{index}')


def delete_all_bids(request, index):
    Bid.objects.filter(product=products[index]).delete()
    return HttpResponseRedirect('/products/0')

def get_info(request, product_id):
    products = Product.objects.all()
    bids = Bid.objects.filter(product=products[product_id])
    bid_data = list(bids.values('user__fullname', 'bid_amount', 'bid_time'))
    return JsonResponse(bid_data, safe=False)



