import os
from pathlib import Path
from os import environ
from dotenv import load_dotenv

# import finance.apps
# import servers.apps

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = environ.get('DJANGO_SECRET_KEY')

DEBUG = True

if not DEBUG:
    CSRF_COOKIE_SECURE = True  #to avoid transmitting the CSRF cookie over HTTP accidentally.
    SESSION_COOKIE_SECURE = True  #to avoid transmitting the session cookie over HTTP accidentally.
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    ALLOWED_HOSTS = ["194.146.123.65", "admin-napsv.ir"]
else:
    ALLOWED_HOSTS = ['127.0.0.1', "*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'rest_framework',
    'django_celery_beat',
    'accounts.apps.AccountsConfig',
    "bot_connection.apps.BotConnectionConfig",
    "bot_customers.apps.BotCustomersConfig",
    "bot_finance.apps.BotFinanceConfig",
    "bot_reports.apps.BotReportsConfig",
    "sellers_finance.apps.SellersFinanceConfig",
    "sellers_reports.apps.SellersReportsConfig",
    'servers.apps.ServersConfig',
    'bot_config.apps.BotConfigConfig',
    'sellers_config.apps.SellersConfigConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'HiddifyPanel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates',
                 BASE_DIR / 'accounts/templates',
                 ]
        ,
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

WSGI_APPLICATION = 'HiddifyPanel.wsgi.application'

AUTH_USER_MODEL = 'accounts.User'
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hiddify',
        'USER': environ.get("MYSQL_USERNAME"),
        'PASSWORD': environ.get("MYSQL_PASS"),
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            "charset": "utf8mb4",
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = environ.get('STATIC_ROOT')
STATICFILES_FINDERS = ("compressor.finders.CompressorFinder",)
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)


MEDIA_URL = '/media/'
MEDIA_ROOT = environ.get('MEDIA_ROOT')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
