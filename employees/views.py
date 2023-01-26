from django.contrib.auth import authenticate, login, logout, user_logged_in, user_logged_out, get_user
from django.contrib import messages
from django.shortcuts import render, resolve_url, redirect
from .models import Employee as em
from home.models import Sys_Settings
from emp import settings as app_settings
from datetime import datetime
import os
from .forms import EmployeeEditForm
from django.core.files.storage import FileSystemStorage


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
    for e in emplist:
        try:
            if e.end_date < today:
                emplist.remove(e)
        except Exception as e:
            pass
#     emplist = [e for e in emplist if e.end_date >= today]
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


def update_employee(id:int, data_record:EmployeeEditForm)->bool:
    result = False
    try:
        e = em.objects.get(emp_id=id)
        e.first_name = data_record.instance.first_name
        e.last_name = data_record.instance.last_name
        e.position = data_record.instance.position
        e.start_date = data_record.instance.start_date
        e.end_date = data_record.instance.end_date
        e.email = data_record.instance.email
        e.phone = data_record.instance.phone
        e.notes = data_record.instance.notes
        e.department = data_record.instance.department
        e.save()
        result = True
    except Exception as e:
        print(e)
    return result


def employee_edit(request, id):
    si = Sys_Settings()
    if request.method == 'POST':
        emp_id = request.POST['emp_id']
        form = EmployeeEditForm(request.POST, request.FILES)
        if form.is_valid():
            if update_employee(id=emp_id, data_record=form):
                messages.success(request, 'Employee record updated successfully.')
                url = resolve_url('employee', emp_id)
                return redirect(url)

        messages.error(request, 'Employee record update failed.')
        context = {
            'form': form,
            'title': 'Employee Edit',
            'orgname': si.orgname,
            'supportlink': si.supportlink
        }
        messages.success(request, form.errors)
        return render(request, 'employee_edit.html', context=context)

    else:
        e = em.objects.get(emp_id=id)
        e.imagepath = determine_image_path(e.image)
        form = EmployeeEditForm(instance=e)
        context = {
            'form': form,
            'e': e,
            'title': 'Employee Edit',
            'orgname': si.orgname,
            'supportlink': si.supportlink
        }
        return render(request, 'employee_edit.html', context=context)


# only post expected.
def employee_edit_image(request, id):
    if request.method == 'POST':
        # load file name from post data
        file_obj = request.FILES['image']
        file_name = file_obj.name
        file_size = file_obj.size
        print(file_name)
        print(file_size)
        # determine server path for file
        base_folder = app_settings.BASE_DIR
        fullpath = os.path.join(base_folder, 'static', 'images', file_name)
        relative_path = os.path.join('static', 'images', file_name)
        relative_path = relative_path.replace('\\', '/')
        # save file to server
        fs = FileSystemStorage()
        fs.save(fullpath, file_obj)
        # update database record
        e = em.objects.get(emp_id=id)
        e.image = relative_path
        e.save()
        messages.success(request, 'Employee image updated successfully.')
        url = resolve_url('employee', id)
        return redirect(url)
    else:
        url = resolve_url('employee', id)
        return redirect(url)
