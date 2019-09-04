SECRET_KEY = "dump-secret-key"

ROOT_URLCONF = "django_ip_access.urls"

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.admin",
    "django_ip_access",
)

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3"}}
