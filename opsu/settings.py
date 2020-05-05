# -*- coding: utf-8 -*-
"""
Django settings for LOEU project.
"""

# Standard Libraries
import os

# Django Libraries
from django.utils.translation import gettext_lazy as _

# Thirdparty Libraries
import environ

ENVIROMENT = environ.Env()  # set default values and casting
environ.Env.read_env()  # reading .env file

SECRET_KEY = ENVIROMENT("SECRET_KEY")

DEBUG = ENVIROMENT("DEBUG")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

GOOGLE_RECAPTCHA_SECRET_KEY = "6LevF1gUAAAAAPn3z8EswCgIk1S_jLKYdf4s62B9"

PASSWORD_RESET_TIMEOUT_DAYS = 2


ALLOWED_HOSTS = ["127.0.0.1", "localhost", "loe.terna.net", "admin.loe.terna.net"]

##################################### EMAIL CONFIG #####################################
EMAIL_BACKEND = ENVIROMENT("EMAIL_BACKEND")
EMAIL_HOST = ENVIROMENT("EMAIL_HOST")
EMAIL_PORT = ENVIROMENT("EMAIL_PORT")
EMAIL_HOST_USER = ENVIROMENT("EMAIL_USER")
EMAIL_HOST_PASSWORD = ENVIROMENT("EMAIL_PASSWORD")
EMAIL_USE_TLS = True


################################### Data Base CONFIG ###################################
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "USER": ENVIROMENT("DBUSER"),
        "NAME": ENVIROMENT("DBNAME"),
        "PASSWORD": ENVIROMENT("DBPASSWORD"),
        "HOST": ENVIROMENT("DBHOST"),
        "DATABASE_PORT": ENVIROMENT("DBPORT"),
    }
}


################################ Application definition ################################
INSTALLED_APPS = [
    # My apps #
    "globales",
    "oeuacademic",
    "oeuconfig",
    "oeu",
    "cuenta",
    "api_v1",
    ####################
    "dal",
    "dal_select2",
    "suit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "leaflet",
    "djgeojson",
    "ckeditor",
    "rest_framework",
    "corsheaders",
    # 'django.contrib.sites',
    # 'debug_toolbar',
]


SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = "opsu.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [os.path.join(BASE_DIR, "jinja2")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": ["django_settings_export.settings_export"],
            "environment": "opsu.jinja2.environment",
        },
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.csrf",
                "django.template.context_processors.tz",
                "django.template.context_processors.static",
            ]
        },
    },
]

################################## corsheaders Config ##################################
CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST = [
#     "https://example.com",
#     "https://sub.example.com",
#     "http://localhost:8080",
#     "http://127.0.0.1:9000"
# ]

############################## Templates Settings Exports ##############################
NOMBRE_APP = "MPPEU|OPSU|LOEU"
ESLOGAN = ""
PREFIJO = "MPPEU"
SUFIJO = "OPSU"
VERSION = "1.0"
INICIAL_A = "E"
INICIAL_B = "U"

SETTINGS_EXPORT = [
    "NOMBRE_APP",
    "ESLOGAN",
    "PREFIJO",
    "SUFIJO",
    "VERSION",
    "INICIAL_A",
    "INICIAL_B",
]

############################# Django Rest Framework Config #############################
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
}

################################## Map LeftLet Config ##################################
LEAFLET_CONFIG = {
    "DEFAULT_CENTER": (7, -66),
    "DEFAULT_ZOOM": 5,
    "MIN_ZOOM": 1,
    "MAX_ZOOM": 24,
    "OVERLAYS": [],
    "SCALE": "both",
    "TILES": [
        (
            "Mapa",
            "https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}",
            {
                "attribution": 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
                "maxZoom": 24,
                "id": "mapbox.streets",
                "accessToken": "pk.eyJ1IjoiZ3ZpenF1ZWwiLCJhIjoiY2szOWVzMnpvMDFpMDNtbmp0YnAzd2s0NCJ9.q34qYWhksU2bEuTs-UGPAg",
            },
        ),
        (
            "Satélite",
            "https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}",
            {
                "attribution": 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
                "maxZoom": 24,
                "id": "mapbox.streets-satellite",
                "accessToken": "pk.eyJ1IjoiZ3ZpenF1ZWwiLCJhIjoiY2szOWVzMnpvMDFpMDNtbmp0YnAzd2s0NCJ9.q34qYWhksU2bEuTs-UGPAg",
            },
        ),
    ],
    "PLUGINS": {
        "markercluster": {
            "css": ["css/MarkerCluster.Default.css", "css/MarkerCluster.css"],
            "js": "js/leaflet.markercluster.js",
            "auto-include": True,
        }
    },
}

SITE_ID = 1

WSGI_APPLICATION = "opsu.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.UnsaltedMD5PasswordHasher",
]

AUTH_USER_MODEL = "cuenta.Persona"
LOGIN_URL = "cuenta:login"
LOGIN_REDIRECT_URL = "cuenta:perfil"


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "es"
TIME_ZONE = "America/Caracas"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [("es", _("Spanish"))]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

##################################### Stic Config ######################################

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = "media"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")


################################## Suit Admin Config ###################################
SUIT_CONFIG = {
    # header
    "ADMIN_NAME": "OPSU",
    "HEADER_DATE_FORMAT": "l, j. F Y",
    "HEADER_TIME_FORMAT": "H:i",
    # forms
    "SHOW_REQUIRED_ASTERISK": True,  # Default True
    "MENU": (
        {
            "label": "Personas y Grupos",
            "icon": "icon-user",
            "models": ("cuenta.Persona", "auth.group", "admin.LogEntry"),
        },
    ),
    # misc
    "LIST_PER_PAGE": 15,
}


############################# Logger and Debuguing Config ##############################
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler"}},
    "loggers": {
        "email": {"handlers": ["console"], "level": ENVIROMENT("DJANGO_LOG_LEVEL")},
        "comments": {"handlers": ["console"], "level": "DEBUG"},
        "tasks": {"handlers": ["console"], "level": "DEBUG"},
        "notifications": {"handlers": ["console"], "level": "DEBUG"},
        "standart": {"handlers": ["console"], "level": ENVIROMENT("DJANGO_LOG_LEVEL")},
        "validations": {"handlers": ["console"], "level": "DEBUG"},
        "utils": {"handlers": ["console"], "level": "DEBUG"},
    },
}


USE_DJANGO_JQUERY = False
JQUERY_URL = False
