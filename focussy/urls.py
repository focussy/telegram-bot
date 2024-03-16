from django.urls import path, include

urlpatterns = [
    path("docs/", include("focussy.docs.urls")),
    path("", include("focussy.api.urls")),
]
