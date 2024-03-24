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
        if os.environ.get("RUN_MAIN", None) != "true" and settings.BOT_MAIN:
            from focussy.api.telegram.bot import dp, bot
            async def start_bot():

                logger.warning("Starting polling...")
                await dp.start_polling(bot, handle_signals=False)

            if settings.BOT_USE_POLLING:
                threading.Thread(
                    daemon=True, target=asyncio.run, args=(start_bot(),)
                ).start()
            else:
                async def setup_bot():
                    await bot.delete_webhook(drop_pending_updates=True)
                    await bot.set_webhook(settings.WEBHOOK_URL)

                asyncio.run(setup_bot())
