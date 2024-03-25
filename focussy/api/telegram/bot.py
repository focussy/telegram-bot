import logging

import redis.asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from django.conf import settings
from focussy.api.telegram.dialogs.main import main_window as main_window
from focussy.api.telegram.dialogs.stat import stat_window
from focussy.api.telegram.dialogs.task_config import task_config_dialog
from focussy.api.telegram.dialogs.tests import tests_window
from focussy.api.telegram.dialogs.test.dialog import test_dialog
from focussy.api.telegram.middleware import CheckUserMiddleware
from focussy.api.telegram.routers import router as main_router

logger = logging.getLogger(__name__)

