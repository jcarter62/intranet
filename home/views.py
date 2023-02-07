from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse
from .models import File as fm
from .models import Page as pm
from .models import Sys_Settings
import os


# Create your views here.


def home(request):
    # determine page name where page_type = 'M'
    pg = pm.objects.get(page_type='M')
    if pg:
        page_name = pg.name
    else:
        page_name = 'home'
    return homewithpage(request, page_name)


# favicon reference:
# https://adamj.eu/tech/2022/01/18/how-to-add-a-favicon-to-your-django-site/
#
def favicon(request):
    file = (settings.BASE_DIR / 'static' / 'favicon.ico').open("rb")
    return FileResponse(file, content_type='image/x-icon')


# method to return absolute path to file in static folder
def get_static_path(filename):
    parts = filename.__str__().split('/')
    base_folder = settings.BASE_DIR.__str__()
    fullpath = base_folder
    for p in parts:
        if p > '':
            fullpath = os.path.join(fullpath, p)
#    bd = settings.BASE_DIR.__str__() # .replace('\\', '/')
#    filestr = filename.__str__()
#    fullpath = os.path.join(bd, filestr) # .replace('\\', '/')
    return fullpath


def homewithpage(request, page_name):
    # determine title and description for page
    pg = pm.objects.get(name=page_name)
    if pg:
        title = pg.title
        description = pg.description
    else:
        title = page_name
        description = ''

    # determine files for page
    filelist = list(fm.objects.filter(page=page_name))

    for f in filelist:
        # zero pad x.Order and save as f.sortkey
        f.sortkey = str(f.Order).zfill(3) + f.name
        parts = f.file.__str__().split('.')
        ext = parts[len(parts) - 1]
        f.file_exists = False
        if f.filetype == 'F':
            f.islocal = True
            f.file_exists = os.path.exists(get_static_path(f.file))
        else:
            f.islocal = False

        if f.file.name is None:
            f.file_exists = False
        elif f.file.name == '':
            f.file_exists = False

        if f.file_exists:
            f.icon = generate_file_icon(ext)
        else:
            f.icon = generate_file_icon('misssing')

    filelist.sort(key=lambda x: x.sortkey)

    #
    # if local file starts with f, add / to beginning of file name.
    #
    for f in filelist:
        if f.filetype == 'F':
            try:
                if f.file.name[0] == 'f':
                    f.file.name = '/' + f.file.name
            except Exception as e:
                print(e.__str__())

    ss = Sys_Settings()
    context = {
        'files': filelist,
        'title': title,
        'description': description,
        'orgname': ss.get_orgname,
        'supportlink': ss.get_supportlink,
    }
    return render(request, 'home.html', context=context)


def about(request):
    return render(request, 'about.html')


def generate_file_icon(ext):

    def svg_pdf():
        return 'M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3M9.5 11.5C9.5 12.3 8.8 13 8 13H7V15H5.5V9H8C8.8 9 9.5 9.7 9.5 10.5V11.5M14.5 13.5C14.5 14.3 13.8 15 13 15H10.5V9H13C13.8 9 14.5 9.7 14.5 10.5V13.5M18.5 10.5H17V11.5H18.5V13H17V15H15.5V9H18.5V10.5M12 10.5H13V13.5H12V10.5M7 10.5H8V11.5H7V10.5Z'

    def svg_xls():
        return 'M21.17 3.25Q21.5 3.25 21.76 3.5 22 3.74 22 4.08V19.92Q22 20.26 21.76 20.5 21.5 20.75 21.17 20.75H7.83Q7.5 20.75 7.24 20.5 7 20.26 7 19.92V17H2.83Q2.5 17 2.24 16.76 2 16.5 2 16.17V7.83Q2 7.5 2.24 7.24 2.5 7 2.83 7H7V4.08Q7 3.74 7.24 3.5 7.5 3.25 7.83 3.25M7 13.06L8.18 15.28H9.97L8 12.06L9.93 8.89H8.22L7.13 10.9L7.09 10.96L7.06 11.03Q6.8 10.5 6.5 9.96 6.25 9.43 5.97 8.89H4.16L6.05 12.08L4 15.28H5.78M13.88 19.5V17H8.25V19.5M13.88 15.75V12.63H12V15.75M13.88 11.38V8.25H12V11.38M13.88 7V4.5H8.25V7M20.75 19.5V17H15.13V19.5M20.75 15.75V12.63H15.13V15.75M20.75 11.38V8.25H15.13V11.38M20.75 7V4.5H15.13V7Z'

    # ref:
    #
    def svg_default():
        return 'M3.05 13H1V11H3.05C3.5 6.83 6.83 3.5 11 3.05V1H13V3.05C17.17 3.5 20.5 6.83 20.95 11H23V13H20.95C20.5 17.17 17.17 20.5 13 20.95V23H11V20.95C6.83 20.5 3.5 17.17 3.05 13M12 5C8.13 5 5 8.13 5 12S8.13 19 12 19 19 15.87 19 12 15.87 5 12 5M11.13 17.25H12.88V15.5H11.13V17.25M12 6.75C10.07 6.75 8.5 8.32 8.5 10.25H10.25C10.25 9.28 11.03 8.5 12 8.5S13.75 9.28 13.75 10.25C13.75 12 11.13 11.78 11.13 14.63H12.88C12.88 12.66 15.5 12.44 15.5 10.25C15.5 8.32 13.93 6.75 12 6.75Z'

    # ref: paperclip off
    # <svg style="width:24px;height:24px" viewBox="0 0 24 24">
    #     <path fill="currentColor" d="M8.5 5.3L7.16 3.96C7.62 2.26 9.15 1 11 1C13.21 1 15 2.79 15 5V11.8L13.5 10.3V5C13.5 3.62 12.38 2.5 11 2.5S8.5 3.62 8.5 5V5.3M18 6H16.5V13.3L18 14.8V6M22.11 21.46L20.84 22.73L17.62 19.5C16.81 21.55 14.83 23 12.5 23C9.46 23 7 20.54 7 17.5V8.89L1.11 3L2.39 1.73L22.11 21.46M11.5 15.5C11.5 16.05 11.95 16.5 12.5 16.5S13.5 16.05 13.5 15.5V15.39L11.5 13.39V15.5M16.42 18.31L14.73 16.62C14.32 17.43 13.5 18 12.5 18C11.12 18 10 16.88 10 15.5V11.89L8.5 10.39V17.5C8.5 19.71 10.29 21.5 12.5 21.5C14.43 21.5 16.04 20.13 16.42 18.31M10 6.8L11.5 8.3V6H10V6.8Z" />
    # </svg>
    def svg_paperclip_off():
        return 'M8.5 5.3L7.16 3.96C7.62 2.26 9.15 1 11 1C13.21 1 15 2.79 15 5V11.8L13.5 10.3V5C13.5 3.62 12.38 2.5 11 2.5S8.5 3.62 8.5 5V5.3M18 6H16.5V13.3L18 14.8V6M22.11 21.46L20.84 22.73L17.62 19.5C16.81 21.55 14.83 23 12.5 23C9.46 23 7 20.54 7 17.5V8.89L1.11 3L2.39 1.73L22.11 21.46M11.5 15.5C11.5 16.05 11.95 16.5 12.5 16.5S13.5 16.05 13.5 15.5V15.39L11.5 13.39V15.5M16.42 18.31L14.73 16.62C14.32 17.43 13.5 18 12.5 18C11.12 18 10 16.88 10 15.5V11.89L8.5 10.39V17.5C8.5 19.71 10.29 21.5 12.5 21.5C14.43 21.5 16.04 20.13 16.42 18.31M10 6.8L11.5 8.3V6H10V6.8Z'

    result = svg_paperclip_off()

    if ext == 'pdf':
        result = svg_pdf()

    if ext == 'xls' or ext == 'xlsx':
        result = svg_xls()

    return result
