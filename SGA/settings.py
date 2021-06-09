"""
Django settings for SGA project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')
MEDIA_URL = '/media/'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't7dwliwxz85wzm%7u87-&#*0n(#weq571q((%6iol+l%%kdm+x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'rest_framework', #<<-- aplicacion para crear apis
    'aplicaciones.inicio',
    'rangefilter',  # <-   add the app
    'ajax_select',  # <-   add the app
    'django.contrib.admin',
    'django.contrib.humanize', 
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'aplicaciones.empresa',
    'aplicaciones.pago_proveedor',
    'aplicaciones.pedidos',
    'aplicaciones.fuds',
    'aplicaciones.activos',
    'aplicaciones.ods',
    'aplicaciones.plan_de_trabajo.apps.PlanDeTrabajoConfig',
    'aplicaciones.expo',
    'aplicaciones.web',
    'aplicaciones.gasto',
    'aplicaciones.compra',
    'aplicaciones.descargas',
    'aplicaciones.solicitud',
    'aplicaciones.ajustes',
    'tinymce',
    'django_cleanup.apps.CleanupConfig',
]

AUTH_USER_MODEL = 'inicio.User'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SGA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'aplicaciones.web.processors.load_menus',
                'aplicaciones.web.processors.shopin_car',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            
        },
    },
]

WSGI_APPLICATION = 'SGA.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sga',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }

    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'sga',
    #     'USER': 'soporte',
    #     'PASSWORD': 'S1st3m45',
    #     'HOST': 'localhost',
    #     'PORT': '3306',
    # }

}



TINYMCE_DEFAULT_CONFIG = {
    'plugins': "print, preview, paste, importcss, searchreplace, autolink, autosave, save, directionality, code, visualblocks, visualchars, fullscreen, image, link, media, template, codesample, table, charmap, hr, pagebreak, nonbreaking, anchor, toc, insertdatetime, advlist, lists, wordcount, imagetools, textpattern, noneditable, help, charmap, quickbars, emoticons,",
    # 'theme': "advanced",
}
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = "/var/www/SGA/static/"
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR,'static'),
)