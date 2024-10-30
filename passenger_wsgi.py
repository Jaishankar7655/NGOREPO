import os
import sys

# Add your project directory to Python path
sys.path.append(os.getcwd())

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

# Import Django WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()