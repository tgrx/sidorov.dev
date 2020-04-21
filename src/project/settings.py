from os import getenv
from pathlib import Path

import dj_database_url
from dynaconf import settings as _settings

from project.utils.consts import AGE_1DAY
from project.utils.consts import AGE_1MINUTE

PROJECT_DIR = Path(__file__).parent.resolve()
BASE_DIR = PROJECT_DIR.parent.resolve()
REPO_DIR = BASE_DIR.parent.resolve()

SECRET_KEY = _settings.SECRET_KEY

DEBUG = _settings.MODE_DEBUG
CACHING = _settings.MODE_CACHING
PROFILING = _settings.MODE_PROFILING

ALLOWED_HOSTS = _settings.ALLOWED_HOSTS + ["localhost", "127.0.0.1"]

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS_ORDERED = {
    0: "django.contrib.admin",
    10: "django.contrib.auth",
    20: "django.contrib.contenttypes",
    30: "django.contrib.sessions",
    40: "django.contrib.messages",
    50: "django.contrib.staticfiles",
    # --- my applications ---
    1000: "applications.meta.apps.MetaConfig",
    2000: "applications.meta.applications.schedule.apps.ScheduleConfig",
    3000: "applications.portfolio.apps.PortfolioConfig",
    4000: "applications.resume.apps.ResumeConfig",
    5000: "applications.target.apps.TargetConfig",
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
        "DIRS": [PROJECT_DIR / "jinja2",],
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

DATABASE_URL = _settings.DATABASE_URL
if _settings.ENV_FOR_DYNACONF == "heroku":
    DATABASE_URL = getenv("DATABASE_URL")

DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL, conn_max_age=AGE_1MINUTE * 10),
}

if CACHING:
    CACHE_MIDDLEWARE_SECONDS = AGE_1DAY
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache",}}

    if not DEBUG:
        CACHES = {
            "default": {
                "BACKEND": "django_bmemcached.memcached.BMemcached",
                "LOCATION": getenv("MEMCACHEDCLOUD_SERVERS").split(","),
                "OPTIONS": {
                    "username": getenv("MEMCACHEDCLOUD_USERNAME"),
                    "password": getenv("MEMCACHEDCLOUD_PASSWORD"),
                },
            }
        }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"  # XXX: DO NOT EVER THINK ABOUT TOUCHING THIS
LOCAL_TIME_ZONE = _settings.LOCAL_TIME_ZONE

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/assets/"

STATICFILES_DIRS = [
    PROJECT_DIR / "static",
]

STATIC_ROOT = REPO_DIR / ".static"

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

if not DEBUG:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=_settings.SENTRY_DSN,
        integrations=[DjangoIntegration()],
        send_default_pii=True,
    )
