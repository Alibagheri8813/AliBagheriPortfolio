from .base import *  # noqa
from dotenv import load_dotenv
import os

load_dotenv(BASE_DIR / ".env", override=False)

DEBUG = True
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"