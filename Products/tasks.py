
from .models import Product
import pytz
import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import time
import threading
from django.core.mail import EmailMultiAlternatives
import schedule


def send_winner_email(prod_id):
    product = Product.objects.get(id=prod_id)
    winner = product.winner
    if winner:
        mail_subject = 'Congratulations on your auction win!'
        message = render_to_string('checkout.html', {
            'product': product,
        })
        to_email = winner.user.email
        email = EmailMultiAlternatives(
            mail_subject, message, settings.EMAIL_HOST_USER, [to_email]
        )
        email.attach_alternative(message, "text/html")
        email.send()
    else:
        pass


def check_condition_and_execute():
    while True:
    # Your condition checking and code execution logic here
        products = Product.objects.all()
        for product in products:
            startdt_aware = product.startdt.astimezone(pytz.timezone('Asia/Dhaka'))
            end_date = startdt_aware + datetime.timedelta(minutes=30)
            enddt_aware = end_date.astimezone(pytz.timezone('Asia/Dhaka'))
            current_date = datetime.datetime.now()
            current_date_aware = current_date.astimezone(pytz.timezone('Asia/Dhaka'))
            sent = product.mailsent

            if (current_date_aware > enddt_aware) and not sent:

                # Execute your code
                send_winner_email(product.id)
                product.mailsent = True
                product.save()
            else:
                pass
        time.sleep(60)


def start_background_task():
    thread = threading.Thread(target=check_condition_and_execute)
    thread.daemon = True
    thread.start()
