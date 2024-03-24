from django.urls import include, path
from rest_framework.routers import DefaultRouter

from config.settings import TELEGRAM_TOKEN
from focussy.api import views

router = DefaultRouter()

# router.register(r"clients", views.ClientViewSet)
# router.register(r"channels", views.ChannelViewSet)
# router.register(r"opts", views.OptViewSet)
# router.register(r"promocode", views.PromocodeViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("healthcheck", views.healthcheck),
    path(TELEGRAM_TOKEN, views.webhook),
]
