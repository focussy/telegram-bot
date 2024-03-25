from django.conf import settings
from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from focussy.api.telegram.bot import dp, bot

router = APIRouter()


@router.post(f"/{settings.BOT_TOKEN}")
async def webhook(request: Request):
    await dp.feed_raw_update(bot, await request.json())
    return Response(status_code=status.HTTP_200_OK)
