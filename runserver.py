from waitress import serve
from emp.wsgi import application
import os
import logging
from decouple import config

host = config('HOST', 'localhost')
port = config('PORT', '8000')

#logger = logging.getLogger('waitress')
#logger.setLevel(logging.INFO)

serve(application, host=host, port=port, threads=10)
