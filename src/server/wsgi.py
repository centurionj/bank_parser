import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/app/src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings.prod')

application = get_wsgi_application()
