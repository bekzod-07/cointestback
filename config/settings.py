"""
Django settings for config project.
Django 5.2
"""

from pathlib import Path
from datetime import timedelta
from corsheaders.defaults import default_headers, default_methods

# =========================
# BASE
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-jfp6d#h5cl3f)p8@^rvjxwnup)$hc6z1ci%m)u!=5jz)7te#i("

DEBUG = True


# =========================
# HOSTS / NGROK
# =========================

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "*",  # ngrok (dev uchun)
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://*.ngrok-free.app",
]


# =========================
# APPLICATIONS
# =========================

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    # Local apps
    "users",
    "quiz",
]


# =========================
# MIDDLEWARE  (MUHIM!)
# =========================

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # ⚠️ ENG TEPADA
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================
# CORS (React + Ngrok)
# =========================

CORS_ALLOW_ALL_ORIGINS = True  # DEV uchun
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = list(default_headers)
CORS_ALLOW_METHODS = list(default_methods)


# =========================
# URL / WSGI
# =========================

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"


# =========================
# TEMPLATES
# =========================

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


# =========================
# DATABASE
# =========================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# =========================
# PASSWORD VALIDATION
# =========================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# =========================
# INTERNATIONALIZATION
# =========================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True


# =========================
# STATIC
# =========================

STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================
# AUTH / API
# =========================

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",  # hozircha ochiq
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


# =========================
# JWT
# =========================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}


# =========================
# SWAGGER
# =========================

SPECTACULAR_SETTINGS = {
    "TITLE": "CoinTest API",
    "DESCRIPTION": "JWT + Quiz system",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
