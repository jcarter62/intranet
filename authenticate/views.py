import base64
import os

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import authenticate, login, logout, user_logged_in, user_logged_out
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# from django.utils.baseconv import base64

from home.models import Sys_Settings, Session_Info_Data


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
            session_id = request.session._get_or_create_session_key()
            sid = Session_Info_Data(session_id)
            sid.set_session_data('login', username)

            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('/')

    else:
        session_id = request.session._get_or_create_session_key()
        sid = Session_Info_Data(session_id)
        sid.remove_session_data('signup')
        sid.remove_session_data('login')


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

        form_data = {
            'username': username,
            'password': password,
            'password1': password1,
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        # convert form_data to a string
        form_data_string = str(form_data)
        session_id = request.session._get_or_create_session_key()
        sid = Session_Info_Data(session_id)
        sid.set_session_data('signup', form_data_string)

        # load valid_domain from environment variable VALID_DOMAIN
        valid_domain = os.environ.get('VALID_DOMAIN', '')

        # check if email is valid
        # check to see if email domain = valid_domain
        if not email.endswith(valid_domain):
            messages.success(request, 'Email domain is not valid')
            redirect_url = resolve_url('signup')
            return redirect(redirect_url)

        if password == password1:
            user = User.objects.create_user(username=username, password=password,
                                            first_name=first_name, last_name=last_name, email=email)
            try:
                user.save()
                messages.success(request, 'User created')
                return redirect('/')
            except Exception as e:
                messages.success(request, e)
                redirect_url = resolve_url('signup')
                return redirect(redirect)
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
        # check to see if session form_data exists
        session_id = request.session._get_or_create_session_key()
        sid = Session_Info_Data(session_id)
        form_data_string = sid.get_session_data('signup')
        # convert form_data from a string to a dictionary
        if not form_data_string:
            form_data = {
                'username': '',
                'password': '',
                'password1': '',
                'first_name': '',
                'last_name': '',
                'email': '',
            }
        else:
            form_data = eval(form_data_string)

        context = {
            'title': 'Auth Home',
            'orgname': si.orgname,
            'supportlink': si.supportlink,
            'form_data': form_data,
        }
        return render(request, 'auth-signup.html', context=context)

