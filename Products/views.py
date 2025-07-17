from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from .models import Product, Bid
from Authenticate.models import UserProfile
from core.utils import is_mobile_or_tablet
from .bidding import handle_bid_submission, compute_auction_status, get_product_context_data

def prod_red(request, index):
    return HttpResponseRedirect(f'/products/{index}/1')

def products(request, index, scr):
    """
    Renders product details view and handles auction logic.
    """
    product = Product.objects.all()[index]
    user = UserProfile.objects.get(user=request.user) if request.user.is_authenticated else None
    context = get_product_context_data(request, product, index, scr, user)
    template = 'Products/mobile_prod.html' if is_mobile_or_tablet(request) else 'Products/product.html'
    return render(request, template, context)

def left_prod(request, index):
    """
    Renders the left pane product summary.
    """
    product = Product.objects.all()[index]
    urls = [url for url in [product.image_url, product.image_url2, product.image_url3, product.image_url4, product.image_url5] if url]
    context = {
        'desc': product.product_description,
        'urls': urls,
        'highest': max(product.starting_price, product.highest_bid),
        'brandname': product.brand_name,
        'dimensions': product.product_dimensions,
        'index': index,
        'brand_username': product.brand_username,
    }
    return render(request, 'Products/left.html', context)

def right_prod(request, index):
    """
    Renders the right pane product detail with auction status.
    """
    product = Product.objects.all()[index]
    user = UserProfile.objects.get(user=request.user) if request.user.is_authenticated else None
    context = get_product_context_data(request, product, index, 2, user)
    return render(request, 'Products/right.html', context)

def bid(request, index, amount):
    """
    Handles bid submission and cooldown logic.
    """
    product = Product.objects.all()[index]
    user = UserProfile.objects.get(user=request.user)
    success = handle_bid_submission(request, product, user, amount)
    template_index = 2 if is_mobile_or_tablet(request) else 'right'
    return HttpResponseRedirect(f'/products/{index}/{template_index}')


def get_info(request, product_id):
    """
    Returns JSON bid info for a specific product.
    """
    product = Product.objects.all()[product_id]
    bids = Bid.objects.filter(product=product)
    bid_data = list(bids.values('user__fullname', 'bid_amount', 'bid_time'))
    return JsonResponse(bid_data, safe=False)

