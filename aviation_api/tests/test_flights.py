from rest_framework.test import APITestCase
from django.urls import reverse
from django.conf import settings

class TestFlight(APITestCase):

    def setUp(self):
        self.flights_url = reverse('aviation:list_flights')
        self.create_flights_url = reverse('aviation:create_flights')
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_post_flights(self):
        flights_data = 	{
          "departure_airport": "00WI",
          "arrival_airport": "01FA",
          "departure_date": "2023-07-17T08:46:19.451000Z",
          "arrival_date": "2023-07-19T08:46:19.451000Z"
        }
        response = self.client.post(self.create_flights_url, flights_data)

        self.assertEqual(response.status_code, 200)

    def test_post_flights_partial_data(self):
        flights_data ={
          "departure_airport": "00WI",
          "arrival_airport": "01FA"
        }

        response = self.client.post(self.create_flights_url, flights_data, format="json")

        self.assertEqual(response.status_code, 200)


    def get_flights(self):
        response = self.client.get(self.flights_url)

        self.assertEqual(response.status_code, 200)