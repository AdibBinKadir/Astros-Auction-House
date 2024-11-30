from django.shortcuts import render
from .models import Product


# Create your views here.



def products(request, index):
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
    highest_bid = request.user.userprofile.highestbid
    urls = [url for url in urls if url is not None]

    start = products[index].starting_price
    if highest_bid > start:
        highest = highest_bid
    else:
        highest = start
    context = {
        'desc': desc,
        'urls': urls,
        'highest': highest,
        'brandname': brandname,
        'dimensions': dimensions,
    }
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    if 'Mobile' in user_agent:
        template = 'mobile_prod.html'
    elif 'Tablet' in user_agent or 'iPad' in user_agent:
        template = 'mobile_prod.html'
    else:
        template = 'product.html'

    return render(request, template, context)
