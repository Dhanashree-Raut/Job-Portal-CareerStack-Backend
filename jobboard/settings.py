from pathlib import Path
import environ
import os
import dj_database_url

# -----------------------------------------------
# BASE SETUP
# -----------------------------------------------

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECRET_KEY comes from .env — never hardcode this
SECRET_KEY = env('SECRET_KEY')

# DEBUG=True means detailed error pages — always False in production
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = ['*']


# -----------------------------------------------
# APPS
# -----------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',           # Django REST Framework
    'rest_framework_simplejwt', # JWT authentication
    'corsheaders',              # Allow React to talk to Django
    'drf_yasg',                 # Swagger API docs
    'rest_framework_simplejwt.token_blacklist',

    # Our apps
    'accounts',
    'jobs',
    'notifications',
    
]


# -----------------------------------------------
# MIDDLEWARE
# -----------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'corsheaders.middleware.CorsMiddleware',  # Must be before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CorsMiddleware must come before CommonMiddleware
# This allows React (running on different port) to make API requests


ROOT_URLCONF = 'jobboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'jobboard.wsgi.application'


# -----------------------------------------------
# DATABASE — PostgreSQL
# -----------------------------------------------



DATABASES = {
    'default': dj_database_url.parse(env('DATABASE_URL'))
}

# Why PostgreSQL over SQLite?
# PostgreSQL is production-grade, handles multiple users,
# supports advanced queries — SQLite is only for learning/testing


# -----------------------------------------------
# CUSTOM USER MODEL
# -----------------------------------------------

AUTH_USER_MODEL = 'accounts.User'

# Why? Django's default User model has limited fields.
# We need roles (job_seeker, employer, admin) so we
# create our own User model in the accounts app.


# -----------------------------------------------
# JWT AUTHENTICATION
# -----------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Why JWT?
# When a user logs in, they get a token (a long string).
# They send this token with every API request to prove who they are.
# Access token expires in 60 mins, refresh token lasts 7 days.


# -----------------------------------------------
# CORS — Allow React Frontend
# -----------------------------------------------

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React dev server
    #  "https://your-app.vercel.app", 
    "https://job-portal-career-stack-frontend.vercel.app",  # your Vercel URL
    "https://job-portal-careerstack-backend-production.up.railway.app",
    
]


CSRF_TRUSTED_ORIGINS = [
    "https://job-portal-career-stack-frontend.vercel.app",  # your Vercel URL
    "http://localhost:3000",
    "https://job-portal-careerstack-backend-production.up.railway.app",
]

# Add this too — allows all origins for API
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True


# Why CORS? Browsers block requests between different ports by default.
# React runs on port 3000, Django on 8000.
# This setting tells Django to allow React to make requests.


# -----------------------------------------------
# CELERY + REDIS
# -----------------------------------------------

CELERY_BROKER_URL = env('REDIS_URL')
CELERY_RESULT_BACKEND = env('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# BROKER_URL — where Celery looks for tasks (Redis queue)
# RESULT_BACKEND — where Celery stores task results


# -----------------------------------------------
# EMAIL CONFIGURATION
# -----------------------------------------------

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp-relay.brevo.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# We use Gmail SMTP to send real emails.
# EMAIL_HOST_PASSWORD should be a Gmail App Password
# (not your regular Gmail password)


# -----------------------------------------------
# PASSWORD VALIDATION
# -----------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# -----------------------------------------------
# STATIC FILES
# -----------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media files (resumes, profile pictures)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Swagger settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'SWAGGER_USE_COMPAT_RENDERERS': False,  # Add this line
}



