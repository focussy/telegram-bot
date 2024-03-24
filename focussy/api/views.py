import json

from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from focussy.api.telegram.bot import bot, dp


# Create your views here.

def healthcheck(request: HttpRequest) -> HttpResponse:
    return HttpResponse("OK", status=status.HTTP_200_OK)


@csrf_exempt
async def webhook(request: HttpRequest) -> HttpResponse:
    return await dp.feed_webhook_update(bot, json.loads(request.body.decode("utf-8")))
