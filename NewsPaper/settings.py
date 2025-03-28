import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env (убедитесь, что файл .env не попадёт в систему контроля версий)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Секретные данные получаются из переменных окружения
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise Exception("DJANGO_SECRET_KEY не задан в переменных окружения!")

DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# Если DJANGO_ALLOWED_HOSTS не задана, по умолчанию используем '127.0.0.1' и 'localhost'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# ===========================
# Applications
# ===========================
INSTALLED_APPS = [
    # Django's built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'django_apscheduler',

    # For django-allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Your apps
    'news.apps.NewsConfig',
    'appointment',
]

SITE_ID = 1

# ===========================
# Authentication
# ===========================
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # для входа в админку
    'allauth.account.auth_backends.AuthenticationBackend',  # для allauth
]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'

# ===========================
# Middleware
# ===========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # обязательно для allauth
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'NewsPaper.urls'

# ===========================
# Templates
# ===========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # общая папка шаблонов
        'APP_DIRS': True,  # ищет шаблоны в приложениях
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # обязателен для allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'NewsPaper.wsgi.application'

# ===========================
# Database
# ===========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ===========================
# Password Validators
# ===========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ===========================
# Internationalization
# ===========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.environ.get('DJANGO_TIME_ZONE', 'UTC')
USE_I18N = True
USE_TZ = True

# ===========================
# Static Files
# ===========================
STATIC_URL = '/static/'

# ===========================
# Default Primary Key Field Type
# ===========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===========================
# Celery and Redis Settings
# ===========================
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis-19370.c276.us-east-1-2.ec2.cloud.redislabs.com')
REDIS_PORT = os.environ.get('REDIS_PORT', '19370')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', 'NL0FKPbhWxxX8OSIF0qpvp6Vcq36aOYm')

CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = os.environ.get('CELERY_TIMEZONE', 'UTC')

# ===========================
# Email Settings
# ===========================
# Для тестирования используем консольный backend. В продакшене используйте SMTP с настройками ниже.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '1309306@gmail.com')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'LianePinto3!')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER', '1309306@gmail.com')

# ===========================
# Admins and Server Email
# ===========================
ADMINS = [
    ('Vasil', 'electricianv@gmail.com'),
]
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# ===========================
# Django-Allauth Settings
# ===========================
ACCOUNT_ADAPTER = 'news.adapters.MyAccountAdapter'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username', 'password1', 'password2']
ACCOUNT_LOGIN_METHODS = {'username', 'email'}

# ===========================
# APScheduler Settings
# ===========================
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds
