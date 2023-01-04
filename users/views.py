from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializer import RegisterSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response

class RegisterAPI(CreateAPIView):
  queryset = User.objects.all()
  serializer_class = RegisterSerializer

#? register olunca token de bana dönsün diye; 
  def create(self, request, *args, **kwargs):
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      user = serializer.save()
      token = Token.objects.get(user=user)
      data = serializer.data
      data["token"] = token.key
      #? burada data içine token field eklendi.
      headers = self.get_success_headers(serializer.data)
      return Response(data, status=status.HTTP_201_CREATED, headers=headers)
  
  
  
  #? register olunca token oluşması signal ile yapıldığında models.py içinde yazılması lazım ama 
  #? kalabalık olmasın diye signals.py dosyası oluşturulup orada yapmak daha güzel
    
  #! yeni bir user oluşturulduğunda onun için token oluşturması için yazılan metod;
  #! bu bize register olduktan sonra tekrar login sayfasına gitmeden login olmamızı sağlıyor.
  #! bunu da user create ediliğinde dönen Response içine token field'nı ekleyerek yapıyor.
  #* aşağıda yazılan  dj_09 Auth dersinden;
  # def create(self, request, *args, **kwargs):
  #   response = super().create(request, *args, **kwargs)
  #   token = Token.objects.create(user_id=response.data['id'])
  #   response.data['token'] = token.key
  #   #? burada Response içine token field eklendi.
  #   # print(response.data)
  #   return response