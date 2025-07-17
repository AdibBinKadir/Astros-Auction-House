from django.http import JsonResponse
from .models import Product, Bid

def get_info(request, product_id):
    """
    Returns JSON data containing bid information for a specific product.
    """
    try:
        product = Product.objects.all()[product_id]
        bids = Bid.objects.filter(product=product)
        bid_data = list(bids.values('user__fullname', 'bid_amount', 'bid_time'))
        return JsonResponse(bid_data, safe=False)
    except IndexError:
        return JsonResponse({'error': 'Invalid product ID'}, status=404)
