# Configuration Django pour un projet déployé sur Render.
# Utilise les variables d'environnement pour les données sensibles et la config.
# (Assurez-vous d'ajouter les dépendances `whitenoise` et `dj_database_url` à votre projet)

import os
from pathlib import Path

# Répertoire de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Clé secrète de Django (doit rester secrète en production)
SECRET_KEY = os.environ.get('SECRET_KEY', 'votre-cle-secrete-ici')

# Mode debug (False en production pour des raisons de sécurité)
DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't', 'yes', 'oui']

# Hôtes autorisés (domaines/IP autorisés pour ce site Django)
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
# Vous pouvez ajouter d'autres noms de domaine si nécessaire (ex. votre domaine custom)

# Applications installées
INSTALLED_APPS = [
    'orders',  # application interne "orders"
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Middleware (couches de traitement intermédiaire)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # pour servir les fichiers statiques en prod
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Fichier de configuration des URLs du projet
ROOT_URLCONF = 'myproject.urls'  # Remplacez 'myproject' par le nom du module principal de votre projet

# Configuration des templates (gabarits HTML)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # ex: [BASE_DIR / "templates"] si vous avez un répertoire de templates global
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

# Application WSGI (point d'entrée WSGI de l'application)
WSGI_APPLICATION = 'myproject.wsgi.application'  # Remplacez 'myproject' par le nom de votre projet

# Base de données
# Par défaut, utilisation d'une base SQLite locale. 
# Pour passer à PostgreSQL ou autre, configurez la variable d'environnement DATABASE_URL.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Si DATABASE_URL est défini dans l'environnement, on l'utilise pour la configuration (ex: Render Postgres)
if 'DATABASE_URL' in os.environ:
    # Assurez-vous d'avoir installé dj_database_url dans vos dépendances
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# Valideurs de mot de passe (pour une meilleure sécurité utilisateur)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalisation
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True
# (USE_L10N n'est plus nécessaire dans Django 4.x et suivants)

# Fichiers statiques (CSS, JavaScript, images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # répertoires de fichiers statiques en développement
STATIC_ROOT = BASE_DIR / 'staticfiles'    # répertoire où collectstatic rassemble les fichiers pour la prod

# Réglages supplémentaires pour une configuration sécurisée en production
if not DEBUG:
    # Active WhiteNoise pour la gestion optimisée des fichiers statiques (compression, mise en cache)
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    # Se base sur l'en-tête HTTP X-Forwarded-Proto (proxy) pour reconnaître les requêtes HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # Redirige automatiquement les requêtes HTTP vers HTTPS
    SECURE_SSL_REDIRECT = True
    # Cookies sécurisés (transmis uniquement via HTTPS)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # Politique HSTS – force le client à utiliser HTTPS pour les requêtes futures (durée 1 heure ici)
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Variables d'environnement personnalisées (exemple : configuration de services externes)
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN', '')
LEGAL_CHANNEL_ID = os.environ.get('LEGAL_CHANNEL_ID', '')

# Type de champ auto-généré par défaut pour les modèles (Django 3.2+)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
