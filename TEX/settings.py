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
DEBUG = True

TEMPLATE_DEBUG = True

ADMINS = (("Ameera Abdelaziz", "aabdelaz@princeton.edu"),
          ("Laura Xu", "lauraxu@princeton.edu"),
          ("Jeffrey Asala", "jasala@princeton.edu"),
          ("Nicole Loncke", "nloncke@princeton.edu"))

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
    "helloDjango",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_cas.middleware.CASMiddleware',
    'account.middleware.Custom403Middleware',
#     'django.middleware.doc.XViewMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas.backends.CASBackend',
)

CAS_SERVER_URL = 'https://fed.princeton.edu/cas/'
CAS_LOGOUT_COMPLETELY = False
CAS_RETRY_LOGIN = True

ROOT_URLCONF = 'TEX.urls'

WSGI_APPLICATION = 'TEX.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'     #For Heroku
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'webpages/static') 
    , os.path.join(BASE_DIR, 'media')
    )


# Email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = "princeton.tex@gmail.com"
EMAIL_HOST_PASSWORD = "axal@tex"
EMAIL_SUBJECT_PREFIX = "[tex NOTIFICATION: ]"


TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'webpages')]


# Setting for HEROKU
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {'default': dj_database_url.config()}

# Works for local testing
# Comment this out before deploying to Heroku!!!!!!!!!!!!!!!!!!!!!!!!!
# https://docs.djangoproject.com/en/1.6/ref/settings/
#databases

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydatabase',
        'USER': 'tex',
        'PASSWORD': 'axal@tex',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']


MEDIA_ROOT="media"
MEDIA_URL="/media/"
