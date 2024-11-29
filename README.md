# django-ip-access
[![Python 3.11](https://img.shields.io/badge/python-3.9|3.10|3.11|3.12-blue.svg)](https://www.python.org/downloads/release/python-311/) 
[![Django 4.2](https://img.shields.io/badge/django-4.2-blue.svg)](https://docs.djangoproject.com/en/4.2/)
[![Python CI](https://github.com/briefmnews/django-ip-access/actions/workflows/workflow.yaml/badge.svg)](https://github.com/briefmnews/django-ip-access/actions/workflows/workflow.yaml)
[![codecov](https://codecov.io/gh/briefmnews/django-ip-access/branch/master/graph/badge.svg)](https://codecov.io/gh/briefmnews/django-ip-access)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

Access a Django app with authorized IP address


## Installation
Install with [pip](https://pip.pypa.io/en/stable/)
```shell script
pip install django-ip-access
```


## Setup 
In order to make `django-ip-access` works, you'll need to follow the steps below.

### Settings
First you need to add the following to your setings:
```python
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',

    'django_ip_access',
    ...
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    'django_ip_access.middleware.IpAccessMiddleware',
    ...
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    
    'django_ip_access.backends.IpAccessBackend',
    ...
)
```

The optional settings with their default values:
```python
IP_ACCESS_CACHE_KEY_PREFIX = "ip_auth_" # the cache key will be ip_auth_{ip}
IP_ACCESS_CACHE_TTL = 60 # in seconds
```

### Migrations
Next, you need to run the migrations in order to update your database schema.
```shell script
python manage.py migrate
```

### Cache
Beware that `django-ip-access` relies on [Django's cache framework](https://docs.djangoproject.com/en/5.1/topics/cache/#django-s-cache-framework) 
to avoid trying to authenticate unauthenticated users on each request.

## How to use ?
Once you are all set up, when a request to your app is made, the `IpAccessMiddleware` checks
for if the IP address of the request exists in the admin panel and
if the user associated to the IP address is active.

## Future work
* Allow the middleware to only runs for specific routes. This would reduces unnecessary overhead for requests that don't require IP-based authentication.

## Tests
Testing is managed by `pytest`. required packages for testing can be installed with:
```shell script
make install
```
