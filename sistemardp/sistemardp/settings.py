"""
Django settings for sistemardp project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
from datetime import timedelta
import os
from pathlib import Path
from datetime import timedelta
from django.contrib.messages import constants as mensajes_de_error

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-le&@ol0tn&kl&vif@97xpt93jla67cit3g39dghs+==#=7)7#!'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'clientes',
    'peliculas',
    'lobby',
    'carro',
    'pedidos',
    'membership',
    'axes',
    'django_ratelimit',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
    
]
AUTHENTICATION_BACKENDS = [
           
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AXES_IPWARE_META_PRECEDENCE_ORDER = [
    'HTTP_X_REAL_IP'
]

#configuracion django-axes
AXES_FAILURE_LIMIT = 5 # Número máximo de intentos fallidos
AXES_COOLOFF_TIME = timedelta(hours=2) # Tiempo de espera (en horas) después de bloquear
AXES_LOCKOUT_URL = '/bloqueado/'
AXES_ONLY_ADMIN_SITE = False # Si True, solo aplica al /admin
AXES_USE_USER_AGENT = False # Si True, considera el user-agent al rastrear intentos
AXES_HANDLER = 'axes.handlers.database.AxesDatabaseHandler'

#configuracion django-ratelimit
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Lista de proxies de confianza
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
TRUSTED_PROXIES = ['127.0.0.1', '::1']  # Agrega las IPs de tus proxies de confianza


ROOT_URLCONF = 'sistemardp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'carro.context_processor.importe_total_carro', #context para importe total del carro
                'carro.context_processor.calcular_descuento_global', #context para calcular descuento global
            ],
        },
    },
]

WSGI_APPLICATION = 'sistemardp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        
    }
}
AXES_CACHE = 'default'
RATELIMIT_USE_CACHE = 'ratelimit'  # Especifica el backend de caché para ratelimit, redis no puede usar el cache predeterminado
RATELIMIT_VIEW_DECORATORS_ENABLED = True  # Asegúrate de que los decoradores estén habilitados

CACHES = {
        'default': {
                    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                    },
        'ratelimit': {
                    'BACKEND': 'django.core.cache.backends.redis.RedisCache',
                    'LOCATION': 'redis://127.0.0.1:6379/1',  # Base de datos separada para ratelimit, hay que iniciarla en wsl
                    }
        
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Ruta de acceso para archivos estáticos durante el desarrollo
static_dir = os.path.join(BASE_DIR, "sistemardp", "static")

# Ruta de acceso para la recopilación de archivos estáticos de cada aplicacion
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# URL base para archivos estáticos
STATIC_URL = '/static/'

#direccion de archivos multimedia que inserta django/admin
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Envío de correo electrónico
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.office365.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "moises.ramirezr@fgr.org.mx"
EMAIL_HOST_PASSWORD = "2"
DEFAULT_FROM_EMAIL = "moises.ramirezr@fgr.org.mx"

# Mostrar mensajes de error
MESSAGE_TAGS = {
    mensajes_de_error.DEBUG: 'debug',
    mensajes_de_error.INFO: 'info',
    mensajes_de_error.SUCCESS: 'success',
    mensajes_de_error.WARNING: 'warning',
    mensajes_de_error.ERROR: 'danger',
}

STRIPE_PUBLIC_KEY = 'pk_test_51QaKoVRqxbIxbxPxVxeaywNXcl2vgBftk2OfMmR2V3jpfYM1vpwh1RSLNpwv3tbUwE1WP6rIisH2RGOK3AdVH7PB00GQIitpru'
STRIPE_SECRET_KEY = 'sk_test_51QaKoVRqxbIxbxPx9hVgheq48DFGDwu7CIgV9CctHf1O6xT0ISa6stYmb2N9LczQ1d5D13tCMSA4FG2gLTWqGwWB00rfZPMTde'
