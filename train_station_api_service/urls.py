from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def api_root(request):
    return Response({
        "user": {
            "register": request.build_absolute_uri("api/user/register/"),
            "login": request.build_absolute_uri("api/user/token/"),
            "profile": request.build_absolute_uri("api/user/me/")
        },
        "train": {
            "stations": request.build_absolute_uri("api/train/stations/"),
            "routes": request.build_absolute_uri("api/train/routes/"),
            "trains": request.build_absolute_uri("api/train/trains/"),
            "journeys": request.build_absolute_uri("api/train/journeys/")
        },
        "docs": {
            "swagger": request.build_absolute_uri("api/docs/"),
            "redoc": request.build_absolute_uri("api/redoc/")
        }
    })

urlpatterns = [
    path("", api_root, name="api-root"),
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls", namespace="user")),
    path("api/train/", include("train.urls", namespace="train")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
