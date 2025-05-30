from django.urls import path, include
from rest_framework import routers
from .views import (
    StationViewSet,
    RouteViewSet,
    TrainTypeViewSet,
    TrainViewSet,
    CrewViewSet,
    JourneyViewSet,
    OrderViewSet
)

router = routers.DefaultRouter()
router.register("stations", StationViewSet, basename="station")
router.register("routes", RouteViewSet, basename="route")
router.register("train-types", TrainTypeViewSet, basename="traintype")
router.register("trains", TrainViewSet, basename="train")
router.register("crews", CrewViewSet, basename="crew")
router.register("journeys", JourneyViewSet, basename="journey")
router.register("orders", OrderViewSet, basename="order")

app_name = "train"

urlpatterns = [
    path("", include(router.urls)),
]
