from django.urls import path
from .views import FlightMVS, ReservationMVS
from rest_framework import routers


router = routers.DefaultRouter()
router.register("flights", FlightMVS, basename="flights")
router.register("reservations", ReservationMVS)

# urlpatterns = [
  
# ]

# urlpatterns += router.urls

#* sadece aşağıdaki ile çalışır,

urlpatterns = router.urls