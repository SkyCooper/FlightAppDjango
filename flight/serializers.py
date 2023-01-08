from rest_framework import serializers
from .models import Flight, Reservation, Passenger

class FlighSerializer(serializers.ModelSerializer):
  class Meta:
    model = Flight
    fields = (
        "id",
        "flight_number",
        "operation_airlines",
        "departure_city",
        "arrival_city",
        "date_of_departure",
        "etd"
    )
    
    
class PassengerSerializer(serializers.ModelSerializer):    
  class Meta:
    model = Passenger
    fields = "__all__"
    

class ReservationSerializer(serializers.ModelSerializer):
  user = serializers.StringRelatedField()
  # user_id = serializers.IntegerField() #! bu yapmadık çünkü o anda kim reservasyon create ediyorsa ordan çekicez.
  
# ReservationSerializer'ı en basit hali ile yazıp bırakırsak dönen response sadece sayılardan/id'lerden olur.
# bundan dolayı user ve flight sadece id olmasın, modelde tanımlanan str foksiyonundaki gibi görünsün diye
# StringRelatedField() ile düzenleme yapıyoruz. fakat create için kullanılmayacağı için,
# ...._id olarak yeniden tanımlama yapıp  IntegerField yapıyoruz ve fields içine ekliyoruz.

  flight = serializers.StringRelatedField()
  flight_id = serializers.IntegerField()
  
  # passenger 1,2,3 gigi değilde bilgileri ile görünsün diye yukarıda ayrıca bir PassengerSerializer yazdık,
  # ve passenger değişkenini ondan gelen responsa atadık,
  passenger = PassengerSerializer(many=True, # birden fazla objesi olduğundan
                                  # required=True
                                  )
  
  class Meta:
    model = Reservation
    fields = (
        "id",
        "user",
        "flight",
        "flight_id",
        "passenger"
    )
  
  # rezervasyon oluşturulduğunda/post-create edildiğinde;
  # gelen veri içinde rezesvasyonu yapılan yolcuların da bilgileri var, fakat ReservationSerializer'ın kullandığı Reservation modelinde yolcular(passenger) ile ilgili bir field yok,
  # bundan dolayı bir rezervasyon oluşturulduğunda Reservation modelinin kayıt yapacağı Reservation tablosunda yolcular(passenger) için de sütün yok.
  # hata olmaması için create metodunu override etmek gerekiyor.
  # gelen data içerisinden sadece gerekli verilerin alınıp işlenebilmesi için passenger ile ilgili bilgileri çıkarıp rezervasayon modeline yollıcaz,
  # çıkardığımız passenger bilgileri ile de Passenger tablosunda passenger create edicez
  # ve manytomany olduğundan bunları ilişkilendiricez.
  
  # son olarak, data içinde bu reservasyonu create eden user'ın id bilgisi yok, çünkü yukarıda onu user = serializers.StringRelatedField() olarak tanımladık, fakat Reservation create ederken lazım.
  # user_id bilgisinide validated_data içine eklemek için, aktif olan/login olan user'dan alıcaz, 
    
  def create(self, validated_data):
    # passenger bilgilerini çıkarıp bir değişkene atadık.
    passenger_data = validated_data.pop("passenger")
    
    # eksik olan user_id'yi request yapan user'dan alıp data içine ekledik.
    # self.context["request"].user.id --> burası kalıp, ezberden yap.
    validated_data["user_id"] = self.context["request"].user.id
    
    # passenger çıkmış, user_id eklenmiş datadan rezervasyon create ettik.
    reservation = Reservation.objects.create(**validated_data)
    
    
    # yukarıda passenger bilgilerini çıkarıp değişkene atamıştık, onun içindeki her passenger bilgisi için;
    for passenger in passenger_data:
      # Passenger modelinden bir passenger create ediyoruz.
      pas = Passenger.objects.create(**passenger)
      
      #! ilişkilendirme yapılması,(ManytoMany olduğundan özel olarak yapılıyor,)
      # Rezervasyon modelinde passenger field olduğu için (for i in data);
      # i gelecek yere mutlaka passenger yazılması gerekiyor, 
      # reservasyon modelindeki passengere oluşturulan pas(yolcuyu) ekle demek alttaki;
      reservation.passenger.add(pas)
    
    # oluşturulan reservasyon objesini save edip, return yapıyoruz.  
    reservation.save()
    return reservation
  
  
class StaffFlightSerializer(serializers.ModelSerializer):
  
  reservation = ReservationSerializer(many=True, read_only=True)
  
  class Meta:
    model = Flight
    fields = (
        "id",
        "flight_number",
        "operation_airlines",
        "departure_city",
        "arrival_city",
        "date_of_departure",
        "etd",
        "reservation"
    )
  