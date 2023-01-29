"""
WSGI config for emp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emp.settings')
cwd = os.getcwd()
staticpath = os.path.join(cwd, 'static')

application = get_wsgi_application()
application = WhiteNoise(application, root=staticpath)
application.add_files(staticpath, prefix='employees/')
