"""
ASGI config for focussy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import asyncio
import logging
import os
import threading
from contextlib import asynccontextmanager
import redis.asyncio
import django
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from django.conf import settings
from django.core.handlers.asgi import ASGIHandler
from fastapi import FastAPI

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup(set_prefix=False)


def init(app: FastAPI):
    if not settings.BOT_USE_POLLING:
        from focussy.api.fastapi.routes import router

        app.include_router(router)


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.environ.get("RUN_MAIN", None) != "true" and settings.BOT_MAIN:
        from focussy.api.telegram.dialogs.main import main_window as main_window
        from focussy.api.telegram.dialogs.stat import stat_window
        from focussy.api.telegram.dialogs.task_config import task_config_dialog
        from focussy.api.telegram.dialogs.tests import tests_window
        from focussy.api.telegram.dialogs.test.dialog import test_dialog
        from focussy.api.telegram.middleware import CheckUserMiddleware
        from focussy.api.telegram.routers import router as main_router

        r = redis.asyncio.from_url(settings.BOT_STORAGE_BROKER)
        storage = RedisStorage(r, key_builder=DefaultKeyBuilder(with_destiny=True))

        bot = Bot(settings.TELEGRAM_TOKEN)
        dp = Dispatcher(storage=storage)

        setup_dialogs(dp)
        dp.include_routers(
            main_router,
            main_window,
            test_dialog,
            task_config_dialog,
            stat_window,
            tests_window,
        )

        dp.message.middleware(CheckUserMiddleware())
        dp.callback_query.middleware(CheckUserMiddleware())
        logger.warning("Initializing bot...")

        async def start_bot():
            logger.warning("Starting polling...")
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot, handle_signals=False)

        if settings.BOT_USE_POLLING:
            threading.Thread(
                daemon=True, target=asyncio.run, args=(start_bot(),)
            ).start()
        else:

            logger.warning("Setting up webhook...")
            await bot.delete_webhook(drop_pending_updates=True)
            await bot.set_webhook(settings.WEBHOOK_URL)
            app.state.bot = lambda: bot
            app.state.dp = lambda: dp

    yield

    if os.environ.get("RUN_MAIN", None) != "true" and settings.BOT_MAIN:
        await bot.close()


app = FastAPI(lifespan=lifespan)
app.mount("/django", ASGIHandler())

init(app)
