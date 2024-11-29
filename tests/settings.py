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

IP_ACCESS_CACHE_TTL = 60 * 5
IP_ACCESS_CACHE_KEY_PREFIX = "ip_auth_"
