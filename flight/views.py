from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import FlighSerializer, ReservationSerializer, StaffFlightSerializer
from .models import Flight, Reservation, Passenger
from .permissions import IsStafforReadOnly
from datetime import datetime, date

# Create your views here.
class FlightMVS(ModelViewSet):
  queryset = Flight.objects.all()
  serializer_class = FlighSerializer
  
  # admin olan bütün CRUD işlemlerini yapsın, client sadece görüntüleyebilsin (GET)
  # böyle bir permission olmadığından, permissions.py oluşturup
  # içine IsAdminUser dan faydalanıp Custom bir permission yazdık ve import edip kullandık
  permission_classes = (IsStafforReadOnly,)
  
  def get_serializer_class(self):
    serializer = super().get_serializer_class()
    if self.request.user.is_staff:
      return StaffFlightSerializer
    return serializer
  
  def get_queryset(self):
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    today = date.today()
    if self.request.user.is_staff:
      return super().get_queryset()
    else:
      queryset = Flight.objects.filter(date_of_departure__gt = today)
      if Flight.objects.filter(date_of_departure = today):
        today_qs =  Flight.objects.filter(date_of_departure = today).filter(etd__gt=current_time)
        queryset = queryset.union(today_qs)
      return queryset
  
  
class ReservationMVS(ModelViewSet):
  queryset = Reservation.objects.all()
  serializer_class = ReservationSerializer

# Yukarıdaki hali ile her kullanıcı (admin veya normal) her rezervasyonu görüyor.
# Admin olan (staff) herşeyi görsün, normal olan (client) sadece kendi rezervasyonun görsün diye değişiklik yapıyoruz,
# burada permission kullanmıyoruz çüknkü, permission olunca görsün/görmesin gibi bir ayrım var,
# filitreleme kullanıyoruz, çünkü her halükarda görecek ama filitreli görecek,(gerekli olan kadar görecek)
# eğer staff ise bütün queryset'in taamamını görsün,
# client ise; user'ı request yapan user'sa yani kendisi ise queryset içinden o kadarını görsün,

  
  def get_queryset(self):
    queryset = super().get_queryset()
    if self.request.user.is_staff:
      return queryset
    return queryset.filter(user = self.request.user)