from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from .models import UserProfile
from .tokens import email_verification_token
from .emails import send_verification_email, send_password_reset_email
from core.utils import is_mobile_or_tablet


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user_profile = UserProfile.objects.get(user=user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse("Reset link is invalid!")

    if email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        user_profile.verified = True
        user_profile.save()
        return redirect("/")

    return HttpResponse("Reset link is invalid!")


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse("Activation link is invalid!")

    if request.method == "POST":
        password = request.POST.get("newpass1")
        confirm = request.POST.get("newpass2")
        if password != confirm:
            messages.error(request, "Passwords do not match")
            return render(request, "resetpass.html")

        if email_verification_token.check_token(user, token):
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect("/")

        return HttpResponse("Activation link is invalid!")

    if email_verification_token.check_token(user, token):
        login(request, user)
        return render(request, "resetpass.html")

    return HttpResponse("Activation link is invalid!")


def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm = request.POST.get("password-conf")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        email = request.POST.get("email")
        fullname = request.POST.get("fullname")

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "register.html")

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user, phone=phone, address=address, fullname=fullname)
            send_verification_email(request, user)
            messages.success(request, "Account created. Check your email (or spam).")
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")

    return render(request, "register.html")


def login_user(request):
    template = "mobile_login.html" if is_mobile_or_tablet(request) else "login.html"

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")
        messages.error(request, "Invalid credentials")

    return render(request, template)


def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("/")

    template = "mobile_logout.html" if is_mobile_or_tablet(request) else "logout.html"
    return render(request, template)


def forgotpassword(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            profile = UserProfile.objects.get(user=user)
            if not profile.verified:
                messages.error(request, "Email was never verified")
            else:
                send_password_reset_email(request, user)
                messages.success(request, "Check your email for password reset link")
        except User.DoesNotExist:
            messages.error(request, "Email not found")

    return render(request, "forgotpassword.html")

