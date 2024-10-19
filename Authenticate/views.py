from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



def login_user(request):
    messages = []
    user = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.append('Invalid credentials')
            return render(request, 'login.html', {'messages': messages})
    else:
        return render(request, 'login.html', {'messages': messages})
    

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def register_user(request):
    messages = []
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_conf')
        if password == password_confirm:
            user = User.objects.create_user(username, email, password)
            user.save()
            messages.append('User created successfully')
        else:
            messages.append('Passwords do not match')
    else:
        pass
    return render(request, 'register.html', {'messages': messages})

