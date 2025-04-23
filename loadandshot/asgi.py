"""
ASGI config for Load&Shot project.
Expose la variable ASGI `application` pour les déploiements asynchrones.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loadandshot.settings')
application = get_asgi_application()
