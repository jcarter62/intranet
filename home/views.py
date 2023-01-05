from django.shortcuts import render
from .models import File as fm

# Create your views here.

def home(request):
    return homewithpage(request, 'top')


#   path('home/<str:page>/', views.homewithpage),
def homewithpage(request, page):
    filelist = list(fm.objects.filter(page=page))
    filelist.sort(key=lambda x: str(x.Order) + x.page + x.name)
    for f in filelist:
        if f.filetype == 'F':
            f.islocal = True
        else:
            f.islocal = False

    context = {
        'files': filelist
    }
    return render(request, 'home.html', context=context)


def about(request):
    return render(request, 'about.html')
