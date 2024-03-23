import logging

import redis.asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from django.conf import settings
from focussy.api.telegram.dialogs.main import main_window as main_window
from focussy.api.telegram.dialogs.stat import stat_window
from focussy.api.telegram.dialogs.task import main_window as task_window
from focussy.api.telegram.dialogs.tests import tests_window
from focussy.api.telegram.middleware import CheckUserMiddleware
from focussy.api.telegram.routers import router as main_router

logger = logging.getLogger(__name__)

redis = redis.asyncio.from_url(settings.BOT_STORAGE_BROKER)
storage = RedisStorage(redis, key_builder=DefaultKeyBuilder(with_destiny=True))

bot = Bot(settings.TELEGRAM_TOKEN)
dp = Dispatcher(storage=storage)

setup_dialogs(dp)
dp.include_routers(main_router, main_window, stat_window, tests_window, task_window)

dp.message.middleware(CheckUserMiddleware())
dp.callback_query.middleware(CheckUserMiddleware())
logger.warning("Initializing bot...")
