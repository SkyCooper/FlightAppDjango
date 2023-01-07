from django.db import models
from django.contrib.auth.models import User

class Flight(models.Model):
  flight_number = models.CharField(max_length=10)
  operation_airlines = models.CharField(max_length=15)
  departure_city = models.CharField(max_length=30)
  arrival_city = models.CharField(max_length=30)
  date_of_departure = models.DateField()
  etd = models.TimeField() # estimated departure
  
  # Rezervation tablosundaki releted_name=reservation'dan dolayı;
  # reservation = ..... (arka planda sanki burada böyle bir field varmış gibi davranır)
  # Flight.reservation ile artık uçuştaki rezervasyonlara ulaşılabilir.

  def __str__(self):
      return f'{self.flight_number} - {self.departure_city} - {self.arrival_city}'

      
class Passenger(models.Model):
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=40)
  email = models.EmailField()
  phone_number = models.IntegerField()
  create_date = models.DateTimeField(auto_now_add=True)
  # Rezervation tablosundaki releted_name=reservations'dan dolayı;
  # reservations = ..... (arka planda sanki burada böyle bir field varmış gibi davranır)
  # Passenger.reservations ile artık yolcuların rezervasyonlarına ulaşılabilir.

  def __str__(self):
      return f'{self.first_name} {self.last_name}'
    

class Reservation(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  # bir reservasyon sadece 1 user tarafından create edileceğinden 1to1, yani foreignkey,
  # ve rezervasyon yapan user silinince, ona ait rezervasyon da silinsin.
  
  passenger = models.ManyToManyField(Passenger, related_name="reservations")
  # bir yolcunun birden fazla rezervasyonu olabilir, bugün, yarın, sonraki hafta vs..
  # ve bir rezervasyon içinde birden fazla yolcu olabilir, kendisi,eşi,çocuğu vs.
  # on_delete belirtilmiyor ManyToManyField de, çünkü mesela eş silindi ama kendisi ve çocuk duruyor.
  # child tablodan parente ulaşabiliyoruz, fakat parentten childe ulaşmak için related_name= "" kullanmak gerekiyor.
  
  flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="reservation")
  # bir rezervasyon sadece bir uçuşta oalbilir, TK212 seferinde gibi (bu örnekte böyle)
  # uçuş silinirse, rezervasyonda silinsin
  # child tablodan parente ulaşabiliyoruz, fakat parentten childe ulaşmak için related_name= "" kullanmak gerekiyor.
  # Flight tablosunda reservasa ile ilgili bir field yok, fakat artık reservation keyword ile ulaşılabilir.
  
  
  def __str__(self):
    return f'{self.user} {self.flight}'