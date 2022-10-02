from itertools import chain

import dj_database_url
from django.urls import reverse_lazy

from project.config import Config
from project.utils import dirs
from project.utils.consts import AGE_1MINUTE

conf = Config()

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SECRET_KEY = conf.SECRET_KEY

DEBUG = conf.MODE_DEBUG
CACHING = conf.MODE_CACHING
PROFILING = conf.MODE_PROFILING

if not DEBUG:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    assert conf.SENTRY_DSN, "Sentry MUST be configured for prod mode"

    sentry_sdk.init(
        dsn=conf.SENTRY_DSN,
        integrations=[DjangoIntegration()],
        send_default_pii=True,
    )

INTERNAL_IPS = [
    "127.0.0.1",
]

INTERNAL_HOSTS = [
    "localhost",
]

ALLOWED_HOSTS = list(chain(conf.ALLOWED_HOSTS or [], INTERNAL_IPS, INTERNAL_HOSTS))

INSTALLED_APPS_ORDERED = {
    0: "django.contrib.admin",
    10: "django.contrib.auth",
    20: "django.contrib.contenttypes",
    30: "django.contrib.sessions",
    40: "django.contrib.messages",
    50: "django.contrib.staticfiles",
    60: "django.contrib.sites",
    # --- 3dp applications ---
    100: "rest_framework",
    101: "rest_framework.authtoken",
    200: "drf_yasg",
    # --- my applications ---
    1000: "applications.onboarding.apps.OnboardingConfig",
    2000: "applications.meta.apps.MetaConfig",
    3000: "applications.meta.applications.schedule.apps.ScheduleConfig",
    4000: "applications.portfolio.apps.PortfolioConfig",
    5000: "applications.resume.apps.ResumeConfig",
    6000: "applications.target.apps.TargetConfig",
    8000: "applications.api.apps.ApiConfig",
}

if PROFILING:
    INSTALLED_APPS_ORDERED[49] = "silk"

INSTALLED_APPS = [app for _, app in sorted(INSTALLED_APPS_ORDERED.items())]

MIDDLEWARE_ORDERED = {
    0: "django.middleware.security.SecurityMiddleware",
    10: "whitenoise.middleware.WhiteNoiseMiddleware",
    20: "django.contrib.sessions.middleware.SessionMiddleware",
    30: "django.middleware.common.CommonMiddleware",
    40: "django.middleware.csrf.CsrfViewMiddleware",
    50: "django.contrib.auth.middleware.AuthenticationMiddleware",
    60: "django.contrib.messages.middleware.MessageMiddleware",
    70: "django.middleware.clickjacking.XFrameOptionsMiddleware",
    80: "django.contrib.sites.middleware.CurrentSiteMiddleware",
}

if PROFILING:
    MIDDLEWARE_ORDERED[71] = "silk.middleware.SilkyMiddleware"
    SILKY_PYTHON_PROFILER = True
    SILKY_PYTHON_PROFILER_BINARY = True

if CACHING:
    MIDDLEWARE_ORDERED[29] = "django.middleware.cache.UpdateCacheMiddleware"
    MIDDLEWARE_ORDERED[31] = "django.middleware.cache.FetchFromCacheMiddleware"

MIDDLEWARE = [mw for _, mw in sorted(MIDDLEWARE_ORDERED.items())]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [
            dirs.DIR_PROJECT / "jinja2",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "environment": "project.utils.xtemplates.build_jinja2_environment",
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "project.utils.xtemplates.user_hour",
                "project.utils.xtemplates.big_brother",
            ],
        },
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
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

WSGI_APPLICATION = "project.wsgi.application"

DATABASE_URL = conf.DATABASE_URL

DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL, conn_max_age=AGE_1MINUTE * 10),
}

# if CACHING:
#     CACHE_MIDDLEWARE_SECONDS = AGE_1DAY
#     CACHES = {
#         "default": {
#             "BACKEND": "django.core.cache.backends.dummy.DummyCache",
#         }
#     }
#
#     if not DEBUG:
#         CACHES = {
#             "default": {
#                 "BACKEND": "django_bmemcached.memcached.BMemcached",
#                 "LOCATION": getenv("MEMCACHEDCLOUD_SERVERS", "").split(","),
#                 "OPTIONS": {
#                     "username": getenv("MEMCACHEDCLOUD_USERNAME"),
#                     "password": getenv("MEMCACHEDCLOUD_PASSWORD"),
#                 },
#             }
#         }

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

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = conf.TIME_ZONE

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/assets/"

STATICFILES_DIRS = [
    dirs.DIR_PROJECT / "static",
]

STATIC_ROOT = dirs.DIR_REPO / ".static"

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOGIN_URL = reverse_lazy("onboarding:sign_in")
LOGIN_REDIRECT_URL = reverse_lazy("onboarding:me")

SITE_ID = conf.SITE_ID

EMAIL_HOST = conf.EMAIL_HOST
EMAIL_HOST_PASSWORD = conf.EMAIL_HOST_PASSWORD
EMAIL_HOST_USER = conf.EMAIL_HOST_USER
EMAIL_PORT = conf.EMAIL_PORT
EMAIL_USE_SSL = conf.EMAIL_USE_SSL
EMAIL_USE_TLS = conf.EMAIL_USE_TLS

EMAIL_FROM = conf.EMAIL_FROM

CELERY_BEAT_CALSYNC = conf.CELERY_BEAT_CALSYNC

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Token": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
    },
}
