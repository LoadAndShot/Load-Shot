"""
WSGI config for Load&Shot project.
Expose la variable WSGI `application` pour le déploiement web.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loadandshot.settings')
application = get_wsgi_application()

