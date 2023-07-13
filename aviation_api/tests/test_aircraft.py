from rest_framework.test import APITestCase
from django.urls import reverse
from django.conf import settings


class TestAircraft(APITestCase):

    def setUp(self):
        self.aircrats_url = reverse('aviation:list_create_aircraft')
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_post_aircraft(self):
        aircraft_data = {
            "serial_number": "30000",
            "manufacturer": "Airforce"
        }

        response = self.client.post(self.aircrats_url, aircraft_data, format="json")

        self.assertEqual(response.status_code, 201)

    def test_update_aircraft(self):
        aircraft_data = {
            "manufacturer": "Airforce"
        }
        url = self.aircrats_url + "30000"
        response = self.client.put(url, aircraft_data, format="json")

        self.assertEqual(response.status_code, 200)
