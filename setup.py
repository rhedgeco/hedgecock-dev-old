from setuptools import setup

setup(
    name='hedgecock_dev',
    version='1.0.0',
    install_requires=[
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "cachecontrol",
        'google',
        'requests',
        'sanic',
        'websockets',
        'dataclasses',
        'jinja2'
    ]
)