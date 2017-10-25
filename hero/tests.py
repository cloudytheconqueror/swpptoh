import json

from django.forms.models import model_to_dict
from django.test import Client, TestCase

from .models import Hero

# Create your tests here.
class HeroTestCase(TestCase):
    def setUp(self):
        Hero.objects.create(name='Superman')
        Hero.objects.create(name='Batman')
        Hero.objects.create(name='Joker')

        self.client = Client()

    def test_hero_str(self):
        batman = Hero.objects.get(name='Batman')
        self.assertEqual(str(batman), 'Batman')

    def test_hero_detail_get(self):
        # Test heroDetail with GET request
        response = self.client.get('/api/hero/1')

        data = json.loads(response.content.decode())  # Deserialize response data
        self.assertEqual(data['name'], 'Superman')  # Verify the data
        self.assertEqual(response.status_code, 200)  # Check the response code

