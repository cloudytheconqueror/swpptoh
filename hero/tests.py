import json

from django.forms.models import model_to_dict
from django.test import Client, TestCase

from .models import Hero


# Create your tests here.
class HeroTestCase(TestCase):
    def setUp(self):
        Hero.objects.create(name='Karkat')
        Hero.objects.create(name='Terezi')
        Hero.objects.create(name='Vriska')

        self.client = Client()

    def test_hero_str(self):
        terezi = Hero.objects.get(name='Terezi')
        self.assertEqual(str(terezi), 'Terezi')

    def test_hero_list_get(self):
        response = self.client.get('/api/hero/')
        data = json.loads(response.content.decode())
        self.assertEqual(len(data), 3)

    def test_hero_list_post(self):
        aradia = json.dumps({'name': 'Aradia'})
        response = self.client.post('/api/hero/', aradia, content_type='application/json')
        self.assertEqual(response.status_code, 201)  # Created

        response = self.client.get('/api/hero/')
        data = json.loads(response.content.decode())
        self.assertEqual(len(data), 4)

        response = self.client.get('/api/hero/4')
        data = json.loads(response.content.decode())
        self.assertEqual(data['name'], 'Aradia')

    def test_hero_list_not_allowed(self):
        response = self.client.put('/api/hero/')
        self.assertEqual(response.status_code, 405)  # Not allowed

    def test_hero_detail_get(self):
        # Test heroDetail with GET request
        response = self.client.get('/api/hero/1')
        data = json.loads(response.content.decode())  # Deserialize response data
        self.assertEqual(data['name'], 'Karkat')  # Verify the data
        self.assertEqual(response.status_code, 200)  # Check the response code

        response = self.client.get('/api/hero/62')
        self.assertEqual(response.status_code, 404)  # Not found

    def test_hero_detail_put(self):
        sollux = json.dumps({'name': 'Sollux'})
        response = self.client.put('/api/hero/3', sollux, content_type='application/json')
        self.assertEqual(response.status_code, 204)  # No content

        response = self.client.get('/api/hero/3')
        data = json.loads(response.content.decode())
        self.assertEqual(data['name'], 'Sollux')

        response = self.client.put('/api/hero/62', sollux, content_type='application/json')
        self.assertEqual(response.status_code, 404)  # Not found

    def test_hero_detail_delete(self):
        response = self.client.delete('/api/hero/3')
        self.assertEqual(response.status_code, 204)  # No content

        response = self.client.get('/api/hero/3')
        self.assertEqual(response.status_code, 404)  # Not found

        response = self.client.delete('/api/hero/62')
        self.assertEqual(response.status_code, 404)  # Not found

    def test_hero_detail_not_allowed(self):
        response = self.client.post('/api/hero/1')
        self.assertEqual(response.status_code, 405)  # Not allowed

