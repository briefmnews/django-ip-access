from setuptools import setup

from os import path

from django_ip_access import __version__

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="django-ip-access",
    version=__version__,
    description="Access a Django app with authorized IP address",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/briefmnews/django-ip-access",
    author="Brief.me",
    author_email="tech@brief.me",
    license="GNU General Public License v3.0",
    packages=["django_ip_access", "django_ip_access.migrations"],
    python_requires=">=3.9",
    install_requires=["Django>=4.2", "django-ipware>=5"],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
    zip_safe=False,
)
