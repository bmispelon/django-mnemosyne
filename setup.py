from setuptools import setup, find_packages
setup(
    name = "django-mnemosyne",
    version = "0.1",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    author = "Baptiste Mispelon",
    author_email = "bmispelon@halike.net",
    url = "http://www.halike.net/mnemosyne/",
    packages=find_packages(),
)
