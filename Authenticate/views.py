from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from .tokens import email_verification_token
from django.conf import settings

def send_verification_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': email_verification_token.make_token(user),
    })
    to_email = user.email
    email = EmailMultiAlternatives(
        mail_subject, message, settings.EMAIL_HOST_USER, [to_email]
    )
    email.attach_alternative(message, "text/html")
    email.send()


def send_password_reset_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Reset your password.'
    message = render_to_string('password_reset_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': email_verification_token.make_token(user),
    })
    to_email = user.email
    email = EmailMultiAlternatives(
        mail_subject, message, settings.EMAIL_HOST_USER, [to_email]
    )
    email.attach_alternative(message, "text/html")
    email.send()


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user_profile = UserProfile.objects.get(user=user)
        user_profile.save()
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        user_profile.verified = True
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('Reset link is invalid!')
    

def reset_password(request, uidb64, token):
    if request.method == 'POST':
        password = request.POST.get('newpass1')
        password_confirm = request.POST.get('newpass2')
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return render(request, 'resetpass.html')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and email_verification_token.check_token(user, token):
            user.set_password(password)
            user.save()
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponse('Activation link is invalid!')
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and email_verification_token.check_token(user, token):
        login(request, user)
        return render(request, 'resetpass.html')
    else:
        return HttpResponse('Activation link is invalid!')



def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password-conf')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        email = request.POST.get('email')
        fullname = request.POST.get('fullname')

        # Validate password confirmation
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')

        # Validate unique username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')

        # Create user and profile
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user, phone=phone, address=address, fullname=fullname)
            messages.success(request, 'User created successfully. Check your email for verification link')
            send_verification_email(request, user)
            return render(request, 'register.html')
        except Exception as e:
            messages.error(request, f'Error creating user: {e}')
   
    return render(request, 'register.html')



def login_user(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    if 'Mobile' in user_agent:
        template = 'mobile_login.html'
    elif 'Tablet' in user_agent or 'iPad' in user_agent:
        template = 'mobile_login.html'
    else:
        template = 'login.html'
    print(template)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, template)
    else:
        return render(request,  template)

    

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/')
    else:
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if 'Mobile' in user_agent:
            template = 'mobile_logout.html'
        elif 'Tablet' in user_agent or 'iPad' in user_agent:
            template = 'mobile_logout.html'
        else:
            template = 'logout.html'
        return render(request, template)
    

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            userprofile = UserProfile.objects.get(user=user)
            if userprofile.verified == False:
                messages.error(request, 'Email was never verified')
                return render(request, 'forgotpassword.html')
            send_password_reset_email(request, user)
            messages.success(request, 'Check your email for password reset link')
            return render(request, 'forgotpassword.html')
        else:
            messages.error(request, 'Email not found')
            return render(request, 'forgotpassword.html')
    else:
        return render(request, 'forgotpassword.html')

