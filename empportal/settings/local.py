from .base import *  # noqa
from .base import env

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="_FHf69b6C-EnylpAz1Fn0_lUKemJqaHR77AgcsMHAM41wiUaQQw",
)

DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080"]
