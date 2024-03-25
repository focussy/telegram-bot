"""
ASGI config for focussy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.conf import settings
from django.core.asgi import get_asgi_application
from fastapi import FastAPI

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
app = FastAPI()


def init(app: FastAPI):
    if not settings.BOT_USE_POLLING:
        from focussy.api.fastapi.routes import router

        app.include_router(router)
        # app.mount(path="/", app=application)


init(app)
