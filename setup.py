from setuptools import setup

setup(
    name="django-ip-access",
    version="1.0.0",
    description="Access a Django app with authorized IP address",
    url="https://github.com/briefmnews/django-ip-access",
    author="Brief.me",
    author_email="tech@brief.me",
    packages=["django_ip_access", "django_ip_access.migrations"],
    python_requires=">=3.7",
    install_requires=["Django>=2.2", "django-ipware>=2.1", "ipaddress>=1"],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
    zip_safe=False,
)
