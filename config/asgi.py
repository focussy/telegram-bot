"""
ASGI config for focussy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

import django
from django.conf import settings
from django.core.handlers.asgi import ASGIHandler
from fastapi import FastAPI

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup(set_prefix=False)


def init(app: FastAPI):
    if not settings.BOT_USE_POLLING:
        from focussy.api.fastapi.routes import router

        app.include_router(router)


app = FastAPI()
app.mount("/django", ASGIHandler())

init(app)
