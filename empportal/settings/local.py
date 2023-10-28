from .base import *  # noqa
from .base import env

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="_FHf69b6C-EnylpAz1Fn0_lUKemJqaHR77AgcsMHAM41wiUaQQw",
)

DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "user@example.com"
DOMAIN = env("DOMAIN")
SITE_NAME = "Leave requests API"
