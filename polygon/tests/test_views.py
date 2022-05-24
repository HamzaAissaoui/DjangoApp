from email import header
from django.test import TestCase
import polygon
from polygon.models import Polygon
from provider.models import Provider
from django.urls import reverse
from django.contrib.gis.geos import Polygon as Poly
from django.utils.encoding import force_text
INVALID_POLYGON_MESSAGE = """Invalid polygon:
                            - coordinates should be in the form [ [ x , y ] , [ x , y ] , [ x , y ] , [ x , y ] ]
                            - first and last point need to have the same coordinates
                            - there should be at least 4 points"""
# Create your tests here.


class PolygonViewGetTest(TestCase):
    field_list = ['p_name', 'price', 'information', 'provider']

    @classmethod
    def setUpTestData(cls):
        # Create 22 polygon for pagination tests
        number_of_polygons = 22
        coordinates = [[1, 1], [1, 6], [6, 6], [1, 1]]
        information = Poly(coordinates)

        for polygon_id in range(number_of_polygons):
            provider = Provider.objects.create(
                name=f'Hamzapoly {polygon_id}',
                email=f'testpoly{polygon_id}@gmail.com',
                phone_number='4084135222',
                language='English',
                currency='EUR')

            Polygon.objects.create(
                p_name=f'poly {polygon_id}',
                price=19.99,
                information=information,
                provider=provider
            )

    def test_pagination_is_twenty(self):
        response = self.client.get(reverse('get-polygons'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 20)

    def test_list_all_polygons(self):
        # Get second page and confirm it has (exactly) remaining 2 items
        response = self.client.get(reverse('get-polygons'), data={'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_geojson_included_in_response_when_listing_all_polygons(self):
        response = self.client.get(reverse('get-polygons'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 20)
        self.assertEqual({'model': 'polygon.polygon', 'pk': 3, 'fields': {'p_name': 'poly 0', 'price': 19.99,
                                                                          'information': 'SRID=4326;POLYGON ((1 1, 1 6, 6 6, 1 1))',
                                                                          'provider': 'Hamzapoly 0'}},
                         response.json()[0])

    def test_list_polygons_by_lat_lng(self):
        response = self.client.get(
            reverse('get-polygons'), data={'lng': 2, 'lat': 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 20)
        self.assertIn({'model': 'polygon.polygon', 'pk': 3, 'fields': {
                      'p_name': 'poly 0', 'price': 19.99, 'provider': 'Hamzapoly 0'}}, response.json())
        # Confirm we're not returning the geojson when we request using lat and lng
        self.assertNotIn('information', response.json()[0]['fields'])

    def test_list_polygons_by_lat_lng_non_existing(self):
        response = self.client.get(
            reverse('get-polygons'), data={'lng': 20, 'lat': 20})
        self.assertEqual(
            force_text(response.content), 'There are no polygons!')
        self.assertEqual(response.status_code, 404)

    def test_get_polygon_by_id_non_existant(self):
        inexistant_id = 25
        response = self.client.get(
            reverse('get-polygon-by-id',  kwargs={'id': inexistant_id}))
        self.assertEqual(
            force_text(response.content), 'Polygon does not exist!')

    def test_get_polygon_by_id_correct(self):
        existing_id = 3
        response = self.client.get(
            reverse('get-polygon-by-id',  kwargs={'id': existing_id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual([{'model': 'polygon.polygon', 'pk': 3, 'fields': {
            'p_name': 'poly 0', 'price': 19.99, 'provider': 'Hamzapoly 0',
            'information': 'SRID=4326;POLYGON ((1 1, 1 6, 6 6, 1 1))'}}], response.json())

    def test_message_no_existing_polygons(self):
        Polygon.objects.all().delete()
        response = self.client.get(reverse('get-polygons'))
        self.assertEqual(
            force_text(response.content), 'There are no polygons!')
        self.assertEqual(response.status_code, 404)


class PolygonViewDeleteTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 1 polygon for delete tests
        coordinates = [[1, 1], [1, 6], [6, 6], [1, 1]]
        information = Poly(coordinates)

        provider = Provider.objects.create(
            name=f'Hamzapoly alternative',
            email=f'testpolyalternative@gmail.com',
            phone_number='4084135222',
            language='English',
            currency='EUR')

        provider = Provider.objects.create(
            name=f'Hamzapoly 23',
            email=f'testpoly23@gmail.com',
            phone_number='4084135222',
            language='English',
            currency='EUR')

        Polygon.objects.create(
            p_name=f'poly 23',
            price=19.99,
            information=information,
            provider=provider
        )

    def test_provider_name_is_required_in_headers(self):
        response = self.client.delete(
            reverse('delete-polygon',  kwargs={'id': 2})
        )
        self.assertEqual(force_text(
            response.content), 'You need to create a provider and add the "name" in headers')

    def test_delete_polygon_by_different_provider(self):
        existant_id = 2
        headers = {'HTTP_NAME': 'Hamzapoly alternative'}
        response = self.client.delete(
            reverse('delete-polygon',  kwargs={'id': existant_id}), **headers)
        self.assertEqual(
            force_text(response.content), 'You are not the creator of this polygon!')

    def test_delete_non_existant_id(self):
        inexistant_id = 24
        headers = {'HTTP_NAME': 'Hamzapoly 23'}
        response = self.client.delete(
            reverse('delete-polygon',  kwargs={'id': inexistant_id}), **headers)
        self.assertEqual(
            force_text(response.content), 'Polygon does not exist!')

    def test_delete_correct_id(self):
        existant_id = 2
        headers = {'HTTP_NAME': 'Hamzapoly 23'}
        response = self.client.delete(
            reverse('delete-polygon',  kwargs={'id': existant_id}), **headers)
        self.assertEqual(
            force_text(response.content), 'Polygon Deleted successfully!')


class PolygonViewUpdateTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 1 polygon for delete tests
        coordinates = [[1, 1], [1, 6], [6, 6], [1, 1]]
        information = Poly(coordinates)

        provider = Provider.objects.create(
            name=f'Hamzapoly 24',
            email=f'testpoly24@gmail.com',
            phone_number='4084135222',
            language='English',
            currency='EUR')

        Provider.objects.create(
            name=f'Hamzapoly 25',
            email=f'testpoly25@gmail.com',
            phone_number='4084135222',
            language='English',
            currency='EUR')

        Polygon.objects.create(
            p_name=f'poly 24',
            price=19.99,
            information=information,
            provider=provider
        )

        Polygon.objects.create(
            p_name=f'poly 25',
            price=19.99,
            information=information,
            provider=provider
        )

    def test_provider_name_is_required_in_headers(self):
        response = self.client.put(
            reverse('update-polygon',  kwargs={'id': 25}))
        self.assertEqual(force_text(
            response.content), 'You need to create a provider and add the "name" in headers')

    def test_update_polygon_by_different_provider(self):
        headers = {'HTTP_NAME': 'Hamzapoly 25'}
        response = self.client.put(
            reverse('update-polygon',  kwargs={'id': 25}), {'p_name': 'test1234'}, **headers)
        self.assertEqual(
            force_text(response.content), 'You are not the creator of this polygon!')

    def test_update_non_existant_id(self):
        inexistant_id = 27
        headers = {'HTTP_NAME': 'Hamzapoly 24'}
        response = self.client.put(
            reverse('update-polygon',  kwargs={'id': inexistant_id}), {'p_name': 'test1234'}, **headers)
        self.assertEqual(
            force_text(response.content), 'Polygon does not exist!')

    def test_update_without_sending_data(self):
        headers = {'HTTP_NAME': 'Hamzapoly 24'}
        response = self.client.put(
            reverse('update-polygon',  kwargs={'id': 25}), **headers)
        self.assertEqual(
            force_text(response.content), 'No data was received')

    def test_update_with_invalid_polygon(self):
        headers = {'HTTP_NAME': 'Hamzapoly 24'}
        response = self.client.put(
            reverse('update-polygon',  kwargs={'id': 25}), data={'coordinates':  [[1, 1], [1, 6], [6, 6], [1, 2]]}, content_type='application/json', **headers)
        self.assertEqual(
            force_text(response.content), INVALID_POLYGON_MESSAGE)

    def test_update_with_correct_inforlation(self):
        headers = {'HTTP_NAME': 'Hamzapoly 24'}
        data = {'p_name': 'hamzaTest222', 'price': 300,
                'coordinates':  [[0, 0], [1, 15], [21, 6], [0, 0]]}
        response = self.client.put(
            reverse('update-polygon',  kwargs={'id': 25}), data=data, content_type='application/json', **headers)
        self.assertEqual(
            response.json()[0], {"model": "polygon.polygon", "pk": 25,
                                 "fields": {"p_name": "hamzaTest222", "price": 300.0,
                                            "information": "SRID=4326;POLYGON ((0 0, 1 15, 21 6, 0 0))",
                                            "provider": "Hamzapoly 24"}
                                 }
        )
