from django.http import HttpRequest, HttpResponse
from rest_framework import status



# Create your views here.


def healthcheck(request: HttpRequest) -> HttpResponse:
    return HttpResponse("OK", status=status.HTTP_200_OK)
