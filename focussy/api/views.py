import asyncio
import json

from asgiref.sync import async_to_sync
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from focussy.api.telegram.bot import bot, dp


# Create your views here.

def healthcheck(request: HttpRequest) -> HttpResponse:
    return HttpResponse("OK", status=status.HTTP_200_OK)


@csrf_exempt
def webhook(request: HttpRequest) -> HttpResponse:
    return asyncio.run(dp.feed_raw_update(bot, json.loads(request.body.decode("utf-8"))))
