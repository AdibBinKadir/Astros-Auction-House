from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

from .tokens import email_verification_token


def send_verification_email(request, user):
    subject = "Verify your account."
    current_site = get_current_site(request)
    message = render_to_string("acc_active_email.html", {
        "user": user,
        "domain": current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": email_verification_token.make_token(user),
    })
    email = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, [user.email])
    email.attach_alternative(message, "text/html")
    email.send()


def send_password_reset_email(request, user):
    subject = "Reset your password."
    current_site = get_current_site(request)
    message = render_to_string("password_reset_email.html", {
        "user": user,
        "domain": current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": email_verification_token.make_token(user),
    })
    email = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, [user.email])
    email.attach_alternative(message, "text/html")
    email.send()
