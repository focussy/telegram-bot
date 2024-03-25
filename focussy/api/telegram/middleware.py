import functools
import logging
from typing import Any, Awaitable, Callable, Dict

import anyio.to_thread
from aiogram import BaseMiddleware
from aiogram.types import Update

from focussy.api.models import Client
from focussy.api.telegram.adapters import run_async
from focussy.api.telegram.utils.consts import USER_NAME, IS_NEW_NAME

logger = logging.getLogger(__name__)


class CheckUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        client, is_new = await run_async(
            Client.objects.get_or_create,
            event.from_user.id,
            defaults={"username": event.from_user.username},
        )
        data[USER_NAME] = client
        data[IS_NEW_NAME] = is_new

        logger.info("Request from user username=%s, new=%s", client.username, is_new)
        await handler(event, data)
