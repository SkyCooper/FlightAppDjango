from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
# resmi doküman : https://www.django-rest-framework.org/api-guide/validators/#validators
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.serializers import TokenSerializer

class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
  # email default required değil, onu değiştirdik, artık zorunlu alan
  # email uniq olsun, değilse validation error dönsün onun için ekledik ve yukarıda import ettik (UniqueValidator)
  password = serializers.CharField(write_only=True, required=True, 
                                   validators=[validate_password], style={"input_type" : "password"} ) 
  # write_only sadece POST, PUT için kullan, GET(yani read) yapılırsa kullanma
  # girilen değer string fakat Django bunu encyript ederek şifreliyor arka planda
  password2 = serializers.CharField(write_only=True, required=True, style={"input_type" : "password"}) 
  # confirmation için tanımlandı, aslında modelde yok onun için zorunlu tanımladık.
  # validators=[validate_password] yazmaya gerek yok zaten ikisini karşılaştırıcaz.
  
  # first_name = serializers.CharField(required=True)
  # first_name zorunlu olsun isteseydik böyle yapmak gerekirdi.
  
  class Meta:
    model = User
    fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'password',
        'password2'
        ]
    # bunlar User model'de olan alanlar, + password2 biz ekledik.
    
  # Object-level validation => https://www.django-rest-framework.org/api-guide/serializers/#object-level-validation
    
  #? Yeni oluşturduğumuz password2 ile password aynımı, bunu konrtol etmek için validate metodunu ekliyoruz.
  #? yazılan metodlarda indentation önemli, class Meta ile aynı hizada,
  def validate(self, data):
    if data['password'] != data['password2']:
        raise serializers.ValidationError(
            {'password': 'Password fields didnt match.'}
        )
    return data
    
  #? ModelSerializer kullanınca create metodu yazmaya gerek yok aslında fakat, User model içinde olmayan bir field 
  #? (password2) kullandığımız için creat metodunu override etmek gerekli;
  def create(self, validated_data): # best practise validated_data yazılır.
    validated_data.pop('password2') # password2 create için gerekli olmadığından dictten çıkardık
    password = validated_data.pop('password') # password sonradan set etmek için dictten çıkardık ve değikene atadık.
    user = User.objects.create(**validated_data) # unpack yapıldı, username=validate_data['username], email = va.......
    # validated_data içinde artık password ve password2 yok, onu kullanarak yeni bir user create edildi.
    user.set_password(password) 
    # yukarıda değişkene atanan password, create edilen user'a atandı,  encrypte olarak db ye kaydedildi.
    user.save()
    # password eklenmiş yeni user save edildi.
    return user
  

class UserTokenSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ("id", "first_name", "last_name", "email")

class CustomTokenSerializer(TokenSerializer):
  user = UserTokenSerializer
  class Meta(TokenSerializer.Meta):
    fields = ("key", "user")
  
  