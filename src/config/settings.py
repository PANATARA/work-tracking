import os
from datetime import timedelta
from pathlib import Path
import sys
import environ

root = environ.Path(__file__) - 2
env = environ.Env()
environ.Env.read_env(env.str(root(), ".env"))

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["https://localhost:8000"])
BASE_DIR = root()

SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.str("ALLOWED_HOSTS", default="").split(",")

# django
INSTALLED_APPS = [
    "core.admin.admin_site.CustomAdminConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
# packages
INSTALLED_APPS += [
    "rest_framework",
    "django_filters",
    "corsheaders",
    "djoser",
    "phonenumber_field",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_extensions",
    "debug_toolbar",
    "django_celery_beat",
]

# apps
INSTALLED_APPS += [
    "apps.api",
    "core",
    "apps.users",
    "apps.projects",
    "apps.activitylog",
    "apps.workspace",
    "apps.offers",
    "apps.notification"
]

# spectacular
INSTALLED_APPS += [
    "drf_spectacular",
]

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]
MIDDLEWARE += [
    "crum.CurrentRequestUserMiddleware",
    "core.middleware.UserMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('PG_DATABASE', default='postgres'),
        'USER': env.str('PG_USER', default='postgres'),
        'PASSWORD': env.str('PG_PASSWORD', default='postgres'),
        'HOST': env.str('DB_HOST', default='pgdb'),
        'PORT': env.str('DB_PORT', default='5432'),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

"""
    DJANGO REST FRAMEWORK
"""

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    #'DEFAULT_PAGINATION_CLASS': 'common.pagination.BasePagination',
}

def show_toolbar(request):
        return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

"""
    LOCALIZATION
"""
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

"""
    Static and Media
"""
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


"""
    CorsHeaders
"""
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]
CSRF_COOKIE_SECURE = False

"""
    DRF SPECTACULAR
"""
SPECTACULAR_SETTINGS = {
    "TITLE": "Pitomets",
    "DESCRIPTION": "Эндпоинты для системы управления проектом",
    "VERSION": "1.0.0",
    "TAGS": [
        {"name": "Authentication & Authorization", "description": "..........................."},
        {"name": "Users -> Profile", "description": "..........................."},
        {"name": "Users -> Settings", "description": "..........................."},

        {"name": "Workspace", "description": "..........................."},

        {"name": "Workspace -> Configuration", "description": "..........................."},
        {"name": "Workspace -> Configuration -> Projects", "description": "..........................."},
        {"name": "Workspace -> Configuration -> Tasks", "description": "..........................."},
        {"name": "Workspace -> Configuration (Personal)", "description": "..........................."},
        {"name": "Workspace: User Favorite", "description": "..........................."},

        {"name": "Workspace -> Member", "description": "..........................."},

        {"name": "Workspace -> Projects", "description": "..........................."},
        {"name": "Workspace -> Projects -> Modules", "description": "..........................."},
        {"name": "Workspace -> Projects -> Tasks", "description": "..........................."},

        {"name": "Workspace -> Projects -> Archived Tasks", "description": "..........................."},
        {"name": "Workspace -> Projects -> Tasks Utils", "description": "..........................."},
        {"name": "Dashboard", "description": "..........................."},

        {"name": "Workspace -> Offer", "description": "..........................."},
        {"name": "User -> Offer", "description": "..........................."},

        {"name": "User -> Task logs", "description": "..........................."},
        {"name": "User -> Notifications", "description": "..........................."},

    ],
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAuthenticated"],
    "SERVE_AUTHENTICATION": ["rest_framework.authentication.BasicAuthentication"],
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": False,
        "displayOperationId": True,
        "syntaxHighlight.active": True,
        "syntaxHighlight.theme": "arta",
        "defaultModelsExpandDepth": -1,
        "docExpansion": "none",
        "displayRequestDuration": True,
        "filter": True,
        "requestSnippetsEnabled": True,
    },
    "COMPONENT_SPLIT_REQUEST": True,
    "SORT_OPERATIONS": False,
    "ENABLE_DJANGO_DEPLOY_CHECK": False,
    "DISABLE_ERRORS_AND_WARNINGS": True,
}

"""
    DJOSER
"""
DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": "#/password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "#/username/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "#/activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": False,
    "SERIALIZERS": {},
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=7),
}

AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = ("apps.users.backends.AuthBackend",)


"""
    ===CELERY SETTINGS===
"""
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL')
CELERY_ACCEPT_CONTENT = env.list('CELERY_ACCEPT_CONTENT', default=['json'])
CELERY_TASK_SERIALIZER = env.str('CELERY_TASK_SERIALIZER', default='json')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND')
CELERY_TIMEZONE = env.str('CELERY_TIMEZONE', default='UTC')
CELERY_BEAT_SCHEDULER = env.str('CELERY_BEAT_SCHEDULER', default='django_celery_beat.schedulers:DatabaseScheduler')


"""
    ===CASHES SETTINGS===
"""
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env.str('CACHE_LOCATION'),
    }
}
