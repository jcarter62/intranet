from waitress import serve
from emp.wsgi import application
import os
import logging

host = os.getenv('HOST', 'localhost')
port = os.getenv('PORT', '8000')

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

serve(application, host=host, port=port, threads=10)
