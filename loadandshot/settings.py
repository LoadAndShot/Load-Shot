"""
Django settings for Load&Shot project.
Ce fichier contient les configurations de l'application Django, y compris
la connexion à la base de données PostgreSQL et les paramètres du projet.
"""
import os
from pathlib import Path

# Chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Clé secrète de Django (définie dans les variables d'environnement en production)
SECRET_KEY = os.environ.get('SECRET_KEY', 'replace-me-in-prod')

# Mode debug (Désactivé en production)
DEBUG = False  # mettre True pour le développement local si nécessaire

# Hôtes autorisés (à ajuster avec le nom de domaine Render le cas échéant)
ALLOWED_HOSTS = ['*']  # En production, spécifier explicitement le host

# Applications installées
INSTALLED_APPS = [
    'orders.apps.OrdersConfig',  # application principale
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # gestion des fichiers statiques en production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'loadshot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # dossier templates global
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'loadshot.wsgi.application'
ASGI_APPLICATION = 'loadshot.asgi.application'

# Base de données (PostgreSQL via DATABASE_URL en production, SQLite en local)
import dj_database_url  # nécessite d'installer le paquet dj-database-url
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Validation des mots de passe utilisateur
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Paramètres de localisation
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# Gestion des fichiers statiques
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # emplacements des fichiers statiques (CSS, JS, images)
STATIC_ROOT = BASE_DIR / 'staticfiles'   # dossier où collectstatic rassemblera les fichiers pour la prod
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuration de redirection après authentification
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

# Clé primaire auto-incrémentée par défaut
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
