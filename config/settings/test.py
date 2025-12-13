"""
Test settings for pytest.
Uses SQLite in-memory database for faster tests.
"""

import tempfile
from pathlib import Path

from .base import *  # noqa

# Use SQLite for testing (faster and no permission issues)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Speed up password hashing for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable logging during tests
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "root": {
        "handlers": ["null"],
    },
}

# Fix drf_yasg deprecation warning
SWAGGER_SETTINGS = {
    **SWAGGER_SETTINGS,
    "USE_COMPAT_RENDERERS": False,
}

# Use a temporary directory for static files during tests to avoid warnings
STATIC_ROOT = Path(tempfile.mkdtemp())
