import logging

import anyio.from_thread
from aiogram.types import Update
from django.conf import settings
from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from focussy.api.telegram.bot import dp, bot

router = APIRouter(prefix="/telegram")

logger = logging.getLogger(__name__)


@router.post(f"/{settings.TELEGRAM_TOKEN}")
def webhook(request: Request):
    try:
        anyio.from_thread.run(
            dp.feed_update,
            bot,
            Update.model_validate(
                anyio.from_thread.run(request.json), context={"bot": bot}
            ),
        )
    finally:
        logger.debug("Handled update")
    return Response(status_code=status.HTTP_200_OK)
