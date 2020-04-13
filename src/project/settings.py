from os import getenv
from pathlib import Path

import dj_database_url
from dynaconf import settings as _settings

PROJECT_DIR = Path(__file__).parent.resolve()
BASE_DIR = PROJECT_DIR.parent.resolve()
REPO_DIR = BASE_DIR.parent.resolve()

SECRET_KEY = _settings.SECRET_KEY

DEBUG = _settings.DEBUG

ALLOWED_HOSTS = _settings.ALLOWED_HOSTS

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
    # --- my apps ---
    1000: "apps.meta.apps.MetaConfig",
    2000: "apps.meta.apps.schedule.apps.ScheduleConfig",
    3000: "apps.portfolio.apps.PortfolioConfig",
    4000: "apps.resume.apps.ResumeConfig",
    5000: "apps.target.apps.TargetConfig",
}

if DEBUG:
    INSTALLED_APPS_ORDERED[41] = "silk"

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

if DEBUG:
    MIDDLEWARE_ORDERED[80] = "silk.middleware.SilkyMiddleware"

MIDDLEWARE = [mw for _, mw in sorted(MIDDLEWARE_ORDERED.items())]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_DIR / "templates", ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "project.utils.xcontext.user_hour",
                "project.utils.xcontext.big_brother",
            ],
            "libraries": {"project_tags": "project.templatetags", },
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

_db_url = _settings.DATABASE_URL
if _settings.ENV_FOR_DYNACONF == "heroku":
    _db_url = getenv("DATABASE_URL")

DATABASES = {
    "default": dj_database_url.parse(_db_url, conn_max_age=600),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"  # XXX: DO NOT EVER THINK ABOUT TOUCHING THIS

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

if DEBUG:
    SILKY_PYTHON_PROFILER = True
    SILKY_PYTHON_PROFILER_BINARY = True
