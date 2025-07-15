from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from Products.models import Product
import datetime
import pytz


def get_time_info():
    """
    Fetches the earliest and latest product start times and formats them for display.
    
    Returns:
        dict: Dictionary containing 'date', 'end_date', 'month', and 'day' in readable format.
    """
    products = Product.objects.all()
    if not products.exists():
        return {
            'date': None,
            'end_date': None,
            'month': None,
            'day': None
        }

    earliest = products.order_by('startdt').first()
    latest = products.order_by('startdt').last()

    server_timezone = pytz.timezone('Asia/Dhaka')
    start_dt = earliest.startdt.astimezone(server_timezone)
    end_dt = (latest.startdt + datetime.timedelta(minutes=30)).astimezone(server_timezone)

    return {
        'date': start_dt.strftime('%b %d, %Y %H:%M:%S'),
        'end_date': end_dt.strftime('%b %d, %Y %H:%M:%S'),
        'month': start_dt.strftime('%B'),
        'day': start_dt.strftime('%d')
    }


def home(request):
    """
    Displays the active countdown with device-specific rendering.
    """
    time_info = get_time_info()
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    if 'Mobile' in user_agent or 'Tablet' in user_agent or 'iPad' in user_agent:
        return redirect('/landing/0')

    return render(request, 'index.html', context={'date': time_info['date']})


def land(request):
    """
    If the user just types the landing URL, redirect to the first product.
    """
    return redirect('/landing/0')


def landing(request, index):
    """
    Displays the landing page with product details based on index and device type.
    
    Args:
        index (int): The index of the product to show.
    """
    products = Product.objects.all()
    time_info = get_time_info()

    if not products.exists():
        return render(request, 'products_dne.html')

    # Clamp index to valid range
    index = max(0, min(index, len(products) - 1))
    selected_product = products[index]

    fs = 3 if len(selected_product.brand_name) > 8 else 6
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    context = {
        'date': time_info['date'],
        'month': time_info['month'],
        'day': time_info['day'],
        'products': products,
        'fs': fs
    }

    if 'Mobile' in user_agent or 'Tablet' in user_agent or 'iPad' in user_agent:
        return render(request, 'mobile_landing.html', context)

    context.update({
        'brandname': selected_product.brand_name,
        'productname': selected_product.product_name,
        'startingprice': selected_product.starting_price,
        'imgurl': selected_product.image_url,
        'index': index
    })

    return render(request, 'landing.html', context)
