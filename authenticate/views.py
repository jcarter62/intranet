from django.contrib.auth.models import User
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import authenticate, login, logout, user_logged_in, user_logged_out
from django.contrib import messages
from home.models import Sys_Settings




def home(request):
    si = Sys_Settings()
    context = {
        'title': 'Auth Home',
        'orgname': si.orgname,
        'supportlink': si.supportlink
    }
    return render(request, 'auth-home.html', context=context)


def login_user(request):
    if request.method == 'POST':
        if request.POST['submit'] == 'register':
            redirect_url = resolve_url('signup')
            return redirect(redirect_url)

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.success(request, 'Username or password is incorrect')
            redirect_url = resolve_url('login')
            return redirect(redirect_url)
        else:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('/')

    else:
        si = Sys_Settings()
        context = {
            'title': 'Auth Home',
            'orgname': si.orgname,
            'supportlink': si.supportlink
        }

        return render(request, 'auth-login.html', context=context)


def logout_user(request):
    if user_logged_in:
        logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('/')
    else:
        messages.success(request, 'You are not logged in')
        return redirect('/')


def signup_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        if password == password1:
            user = User.objects.create_user(username=username, password=password,
                                            first_name=first_name, last_name=last_name, email=email)
            user.save()
            messages.success(request, 'User created')
            return redirect('/')
        else:
            messages.success(request, 'Passwords do not match')
            redirect_url = resolve_url('signup')
            return redirect(redirect_url)

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.success(request, 'Username or password is incorrect')
            redirect_url = resolve_url('login')
            return redirect(redirect_url)
        else:
            login(request, user)
            messages.success(request, 'You are now logged in')
            redirect_url = resolve_url('/')
            return redirect(redirect_url)
    else:
        si = Sys_Settings()
        context = {
            'title': 'Auth Home',
            'orgname': si.orgname,
            'supportlink': si.supportlink
        }
        return render(request, 'auth-signup.html', context=context)
