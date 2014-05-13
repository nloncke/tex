"""
Django settings for TEX project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xqz)1%#98!jgi*pimqwut^sl4tf(i@c*q32)z$djde=$@1&gfw'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True 
DEBUG = False

TEMPLATE_DEBUG = DEBUG

SECRET_AWS_KEY = b'Tx9XGGbYjlp0hDJLmDp9USt9OVm0mTPmy2lvqo4M'

ADMINS = (("Axal", "princeton.tex@gmail.com"),
          ("Ameera Abdelaziz", "aabdelaz@princeton.edu"),
          ("Laura Xu", "lauraxu@princeton.edu"),
          ("Jeffrey Asala", "jasala@princeton.edu"),
          ("Nicole Loncke", "nloncke@princeton.edu"))

MANAGERS = ADMINS

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "account",
    "book",
    "buy",
    "search",
    "sell",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_cas.middleware.CASMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'account.middleware.Custom403Middleware',
    'account.middleware.Custom404Middleware',
    'account.middleware.LoginRequiredMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'account.models.PopulatedCASBackend',
)

ROOT_URLCONF = 'TEX.urls'

WSGI_APPLICATION = 'TEX.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CAS_SERVER_URL = 'https://fed.princeton.edu/cas/'
CAS_REDIRECT_URL = "/"
CAS_LOGOUT_COMPLETELY = True
CAS_RETRY_LOGIN = True

LOGIN_URL="/account/login/"
LOGIN_REDIRECT_URL="/"
LOGOUT_URL = "/"


STATIC_URL = '/static/'
STATIC_ROOT = 'static'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'webpages/fonts')
    , os.path.join(BASE_DIR, 'webpages/less')
    , os.path.join(BASE_DIR, 'webpages/css') 
    , os.path.join(BASE_DIR, 'webpages/js') 
    , os.path.join(BASE_DIR, 'media')
    )


# Email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = "princeton.tex@gmail.com"
EMAIL_HOST_PASSWORD = "axal@tex"
EMAIL_SUBJECT_PREFIX = "[tex notification]: "


TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'webpages')]


# Setting for HEROKU
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {'default': dj_database_url.config()}

# Works for local testing
# Comment this out before deploying to Heroku!!!!!!!!!!!!!!!!!!!!!!!!!
# https://docs.djangoproject.com/en/1.6/ref/settings/
#databases
#        
# DATABASES = {
#     'default': {
#         'ENGINE':'django.db.backends.postgresql_psycopg2',
#         'NAME': 'mydatabase',
#         'USER': 'tex',
#         'PASSWORD': 'axal@tex',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']


MEDIA_ROOT="media"
MEDIA_URL="/media/"
