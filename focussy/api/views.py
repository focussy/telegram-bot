import asyncio
import json

import anyio.to_thread
import anyio.from_thread
from asgiref.sync import async_to_sync
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from focussy.api.telegram.bot import bot, dp


# Create your views here.

def healthcheck(request: HttpRequest) -> HttpResponse:
    return HttpResponse("OK", status=status.HTTP_200_OK)


def webhook_handler(update):
    anyio.from_thread.run(dp.feed_raw_update, bot, update)


@csrf_exempt
async def webhook(request: HttpRequest) -> HttpResponse:
    await anyio.to_thread.run_sync(webhook_handler, json.loads(request.body.decode("utf-8")))
    return HttpResponse("OK", status=status.HTTP_200_OK)
