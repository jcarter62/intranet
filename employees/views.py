from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee as em


# Create your views here.
def employees_all(request):
    emplist = list(em.objects.all())
    for e in emplist:
        x = e.email.split('@')
        e.image = f'images/{x[0]}.jpg'
    # sort emplist by last name and then first name
    emplist.sort(key=lambda x: x.last_name + x.first_name)
    # remove records where current date is after end date
    # determine today's date and store as a string
    today = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
    emplist = [e for e in emplist if e.end_date >= today]
    context = {
        'employees': emplist
    }
    return render(request, 'employees.html', context=context)
    # return render(request, 'employees.html')

# create method to return a single employee with a given id as parameter
def employee(request, id):
    e = em.objects.get(emp_id=id)
    x = e.email.split('@')
    e.image = f'images/{x[0]}.jpg'
    context = {
        'e': e
    }
    return render(request, 'employee.html', context=context)
