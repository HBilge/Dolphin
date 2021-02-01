"""
Django settings for dolphin project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
#import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        "CLIENT": {
            "name": "dolphin",
            "host": "mongodb+srv://dbuserdolphin:dbpassworddolphin@cluster0.h6bhx.mongodb.net/dolphin?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true",
            "username": "dbuserdolphin",
            "password": "dbpassworddolphin",
            "authMechanism": "SCRAM-SHA-1",
        }
    },
    'annotations': {
        "name": "dolphin",
            "host": "mongodb+srv://new_user_587:nXxoVnTlNcva3Mro@cluster0.hngug.mongodb.net/annotations?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true",
            "username": "new_user_587",
            "password": "nXxoVnTlNcva3Mro",
            "authMechanism": "SCRAM-SHA-1",
    }
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'el3v911_hs0e@*0z8op$gn+39ti!db31lkuyg$99lvhdxh(4l*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'articles',
    'ontologies',
    'crispy_forms',
    'storages',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
 #   'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'dolphin.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'dolphin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# STATIC_URL = '/static/'
#
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]


# Configure Django App for Heroku.

#django_heroku.settings(locals())

# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')



AWS_ACCESS_KEY_ID = 'AKIAV2CCWSUXHDR6E3PZ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'dolphin'


AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME


STATIC_URL = "https://dolphin.s3.eu-central-1.amazonaws.com/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
 ]
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'




DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

GRAPH_MODELS = {
    'all_applications':True,
    'group_models':True,
}

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

