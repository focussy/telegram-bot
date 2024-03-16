import asyncio
import logging
import os
import threading

from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "focussy.api"

    def ready(self):
        if os.environ.get("RUN_MAIN", None) != "true":

            async def start_bot():
                from focussy.api.telegram.bot import dp, bot

                logger.warning("Starting polling...")
                await dp.start_polling(bot, handle_signals=False)

            if settings.BOT_USE_POLLING:
                threading.Thread(
                    daemon=True, target=asyncio.run, args=(start_bot(),)
                ).start()
