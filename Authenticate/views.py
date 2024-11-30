from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from django.contrib import messages


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
            messages.success(request, 'User created successfully')
            return redirect('/login/')
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


