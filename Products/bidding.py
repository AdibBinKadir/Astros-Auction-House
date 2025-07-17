import datetime
import pytz
from .models import Bid
from core.utils import get_display_time


def compute_auction_status(user, product, now):
    start_time = product.startdt.astimezone(pytz.timezone("Asia/Dhaka"))
    end_time = start_time + datetime.timedelta(minutes=30)
    if not user or not user.verified:
        return 0 if now < end_time else -1
    if start_time < now < end_time:
        return 1
    return -1

def handle_bid_submission(request, product, user, amount):
    """
    Submits a bid if cooldown allows.
    """
    now = datetime.datetime.now(datetime.timezone.utc).astimezone(pytz.timezone("Asia/Dhaka"))
    existing_bid = Bid.objects.filter(user=user, product=product).first()
    if existing_bid:
        seconds_since = (now - existing_bid.bid_time.astimezone(pytz.timezone("Asia/Dhaka"))).seconds
        if seconds_since < user.cooldown:
            return False
        existing_bid.delete()
    product.highest_bid += amount
    product.winner = user
    product.save()
    Bid.objects.create(user=user, product=product, bid_amount=product.highest_bid - amount, bid_time=now)
    return True

def get_product_context_data(request, product, index, scr, user):
    """
    Reusable product context constructor.
    """
    now = datetime.datetime.now(datetime.timezone.utc).astimezone(pytz.timezone("Asia/Dhaka"))
    startdt = product.startdt.astimezone(pytz.timezone("Asia/Dhaka"))
    enddt = startdt + datetime.timedelta(minutes=30)
    hour, minute, md = get_display_time(startdt)
    auctionable = compute_auction_status(user, product, now)
    bids = [str(bid) for bid in Bid.objects.filter(product=product)]
    fs = 8 if len(product.brand_username) > 8 else 12.5
    W = user and product.winner == user
    context = {
        'desc': product.product_description,
        'urls': [u for u in [product.image_url, product.image_url2, product.image_url3, product.image_url4, product.image_url5] if u],
        'highest': max(product.starting_price, product.highest_bid),
        'brandname': product.brand_name,
        'dimensions': product.product_dimensions,
        'index': index,
        'auctionable': auctionable,
        'bids': bids,
        'end_date': enddt.strftime('%b %d, %Y %H:%M:%S'),
        'scr': scr,
        'winner': product.winner.fullname if product.winner else None,
        'remaining': -5000,
        'brand_username': product.brand_username,
        'verified': user.verified if user else False,
        'W': W,
        'fs': fs,
        'hour': hour,
        'minute': minute,
        'md': md,
    }
    return context
