from django.urls import reverse

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from flight.views import FlightMVS
from flight.models import Flight

from datetime import datetime, date


class FlightTestCase(APITestCase):
  now = datetime.now()
  current_time = now.strftime('%H:%M:%S')
  today = date.today()

  def setUp(self):
    self.factory = APIRequestFactory()
    
    self.flight = Flight.objects.create(
      flight_number='123ABC',
      operation_airlines='THY',
      departure_city='Adana',
      arrival_city='Ankara',
      # date_of_departure='2023-01-08',
      date_of_departure=f'{self.today}',
      # etd='08:35:13')
      etd=f'{self.current_time}')
    
    self.user = User.objects.create_user(
      username = 'admin',
      password = 'admin123*')
    
    self.token = Token.objects.get(user = self.user)
    
  def test_flight_list_as_non_auth_user(self):
    request = self.factory.get('/flight/flights/')
    # print (reverse('flights-list'))
    response = FlightMVS.as_view({'get' : 'list'})(request)
    print(response)
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, 'reservation')
    self.assertEqual(len(response.data), 0)
    
  def test_flight_list_as_staff_user(self):
    request = self.factory.get(
      '/flight/flights/', HTTP_AUTHORIZATION= f'{self.token}')
    self.user.is_staff = True
    self.user.save()
    # force_authenticate(request, user=self.user)
    # request.user = self.user
    response = FlightMVS.as_view({'get' : 'list'})(request)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'reservation')
    self.assertEqual(len(response.data), 1)
    
  def test_flight_create_as_non_auth_user(self):
    request = self.factory.post('/flight/flights/')
    response = FlightMVS.as_view({'post' : 'create'})(request)
    self.assertEqual(response.status_code, 402)
    
  def test_flight_create_as_auth_user(self):
    request = self.factory.post(
      '/flight/flights/', HTTP_AUTHORIZATION= f'{self.token}')
    response = FlightMVS.as_view({'post' : 'create'})(request)
    self.assertEqual(response.status_code, 403)
    
  def test_flight_create_as_staff_user(self):
    data = {
      "flight_number":"123ABC",
      "operation_airlines":"THY",
      "departure_city":"Adana",
      "arrival_city":"Ankara",
      "date_of_departure":"2022-01-08",
      "etd":"16:35:00",
    }
    self.user.is_staff = True
    self.user.save()
    request = self.factory.post(
      '/flight/flights/', data, HTTP_AUTHORIZATION= f'{self.token}')
    response = FlightMVS.as_view({'post' : 'create'})(request)
    self.assertEqual(response.status_code, 201)
    
  def test_flight_update_as_staff_user(self):
    data = {
      "flight_number": "456ewd",
      "operation_airlines": "THY",
      "departure_city": "Adana",
      "arrival_city": "Ankara",
      "date_of_departure": "2022-01-08",
      "etd": "16:35:00",
      }
    print(self.flight.id)

    self.user.is_staff = True
    self.user.save()
    request = self.factory.put(
      '/flight/flights/1/', data, HTTP_AUTHORIZATION=f'Token {self.token}')
    response = FlightMVS.as_view(
      {'put': 'update'})(request, pk='1')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Flight.objects.get('flight_number'), '456ewd')
    

    
    
    
    
    
    
    
    
