# django-ip-access
[![Python 3.11](https://img.shields.io/badge/python-3.9|3.10|3.11|3.12-blue.svg)](https://www.python.org/downloads/release/python-311/) 
[![Django 4.2](https://img.shields.io/badge/django-4.2-blue.svg)](https://docs.djangoproject.com/en/4.2/)
[![Python CI](https://github.com/briefmnews/django-ip-access/actions/workflows/workflow.yaml/badge.svg)](https://github.com/briefmnews/django-ip-access/actions/workflows/workflow.yaml)
[![codecov](https://codecov.io/gh/briefmnews/django-ip-access/branch/master/graph/badge.svg)](https://codecov.io/gh/briefmnews/django-ip-access)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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

### Migrations
Next, you need to run the migrations in order to update your database schema.
```shell script
python manage.py migrate
```

## How to use ?
Once you are all set up, when a request to your app is made, the `IpAccessMiddleware` checks
for if the IP address of the request exists in the admin panel and
if the user associated to the IP address is active.


## Tests
Testing is managed by `pytest`. required packages for testing can be installed with:
```shell script
pytest
```
