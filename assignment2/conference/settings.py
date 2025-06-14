import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from urllib.parse import urlparse, urlunparse
from datetime import timedelta

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env
load_dotenv()

# Load secret key from .env
SECRET_KEY = os.getenv('SECRET_KEY')

# Enable debug mode (should be turned off in production)
DEBUG = True

# Allow all hosts (for development)
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "iscg7420-assignment2-confroom.onrender.com"
]

# Allow all CORS origins (for frontend-backend communication)
CORS_ALLOW_ALL_ORIGINS = True

# Installed apps
INSTALLED_APPS = [
    "corsheaders",  # Support for CORS headers
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "reservation",
]

# Middleware configuration
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # CORS middleware (should be on top)
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Root URL configuration
ROOT_URLCONF = "conference.urls"

# Template engine settings
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI application path
WSGI_APPLICATION = "conference.wsgi.application"

# Default database (loaded from DATABASE_URL)
DATABASES = {
    "default": dj_database_url.config(conn_max_age=600, ssl_require=True)
}

# Override the database name if running tests
if "test" in sys.argv:
    original_url = os.getenv("DATABASE_URL")
    parsed = urlparse(original_url)
    new_db_name = "confroom_db_testing"  # Use a separate database to avoid conflicts
    test_url = urlunparse(parsed._replace(path=f"/{new_db_name}"))
    os.environ["DATABASE_URL"] = test_url
    DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# Skip password validation rules (not needed for this project)
AUTH_PASSWORD_VALIDATORS = []

# Internationalization settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static file settings
STATIC_URL = "static/"

# Default auto-increment primary key field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST framework settings (use JWT authentication)
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ]
}

# SIMPLE_JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_OBTAIN_SERIALIZER": "reservation.serializers.CustomTokenObtainPairSerializer",
}
