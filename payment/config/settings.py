import os
from pathlib import Path

from split_settings.tools import include

include(
    "components/database.py",
    "components/installed_apps.py",
    "components/middleware.py",
    "components/auth_password_validators.py",
    "components/templates.py",
    "components/secret_key.py",
)

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    BASE_DIR / "static",
]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TEMPLATE_DIRS = [os.path.join(BASE_DIR, "templates")]
