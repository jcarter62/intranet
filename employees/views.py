from django.contrib.auth import authenticate, login, logout, user_logged_in, user_logged_out, get_user

from datetime import datetime
from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponse, HttpRequest
from django.forms import forms, CharField
from .models import Employee as em
from home.models import Sys_Settings
from emp import settings as app_settings
import os


def determine_image_path(img) -> str:
    default_image = '/static/images/blank.png'
    base_folder = app_settings.BASE_DIR

    img_file_path = img.__str__()

    fullpath = os.path.join(base_folder, img_file_path)
    # determine if e.imagepath file exists
    if not os.path.isfile(fullpath):
        result = default_image
    else:
        result = '/' + img_file_path

    return result

# Create your views here.
def employees_all(request):
    # set default image
    default_image = '/static/images/blank.png'
    base_folder = app_settings.BASE_DIR


    emplist = list(em.objects.all())
    for e in emplist:
        e.imagepath = determine_image_path(e.image)

    emplist.sort(key=lambda x: x.last_name + x.first_name)
    # remove records where current date is after end date
    # determine today's date and store as a string
    today = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
    emplist = [e for e in emplist if e.end_date >= today]
    si = Sys_Settings()
    context = {
        'employees': emplist,
        'orgname': si.orgname,
        'title': 'Employee List',
        'supportlink': si.supportlink
    }
    return render(request, 'employees.html', context=context)

def get_user_email_address(request):
    results = ''
    user = get_user(request)
    if user.is_superuser:
        results = 'superuser'
    elif user.is_authenticated:
        results = user.email
    return results

# create method to return a single employee with a given id as parameter
def employee(request, id):
    user_email = get_user_email_address(request)
    e = em.objects.get(emp_id=id)
    e.imagepath = determine_image_path(e.image)
    si = Sys_Settings()
    if user_email == 'superuser' or user_email == e.email:
        edit_allowed = True
    else:
        edit_allowed = False
    context = {
        'e': e,
        'title': 'Employee Detail',
        'orgname': si.orgname,
        'supportlink': si.supportlink,
        'edit_allowed': edit_allowed,
    }
    return render(request, 'employee.html', context=context)


def employee_edit(request, id):
    if request.method == 'POST':
        e = em.objects.get(emp_id=id)
        si = Sys_Settings()
        context = {
            'title': 'Employee Edit',
            'orgname': si.orgname,
            'supportlink': si.supportlink
        }
        e.first_name = request.POST['first_name']
        e.last_name = request.POST['last_name']
        e.email = request.POST['email']
        e.phone = request.POST['phone']
        e.position = request.POST['position']
        e.department = request.POST['department']
        e.save()
        redirect_url = resolve_url('employee', id)
        return redirect(redirect_url)
    else:
        e = em.objects.get(emp_id=id)
        e.imagepath = determine_image_path(e.image)
        si = Sys_Settings()
        context = {
            'e': e,
            'title': 'Employee Edit',
            'orgname': si.orgname,
            'supportlink': si.supportlink
        }
        return render(request, 'employee_edit.html', context=context)

