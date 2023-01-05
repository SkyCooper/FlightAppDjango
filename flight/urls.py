from django.urls import path
from .views import FlightMVS, ReservationMVS
from rest_framework import routers


router = routers.DefaultRouter()
router.register("flights", FlightMVS)
router.register("reservations", ReservationMVS)

urlpatterns = router.urls