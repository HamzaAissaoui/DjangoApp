from django.test import TestCase
from polygon.models import Polygon
from provider.models import Provider
from django.contrib.gis.geos import Polygon as Poly

# Create your tests here.


class PolygonModelTest(TestCase):
    field_list = ['p_name', 'price', 'information', 'provider']

    @classmethod
    def setUpTestData(cls):
        coordinates = [ [ 0 , 0 ] , [ 3 , 6 ] , [ 6 , 1 ] , [ 0 , 0 ] ]
        information = Poly(coordinates)
        provider = Provider.objects.create(name='test123', email='test@gmail.com', phone_number='4084132222',
                                           language='French', currency='EUR')
        Polygon.objects.create(p_name='TestPolygon', price=29.59,
                    information=information, provider=provider)

    def test_polygon_object_string(self):
        polygon = Polygon.objects.get(id=1)
        expected_object_name = f"\n- N° {polygon.id}: name = {polygon.p_name!r}, \
                provider_name = {polygon.provider.name!r}, price = {polygon.price!r}"
        self.assertEqual(str(polygon), expected_object_name)

    def test_polygon_name_max_length(self):
        polygon = Polygon.objects.get(id=1)
        max_length = polygon._meta.get_field('p_name').max_length
        self.assertEqual(100, max_length)

    def test_fields_field_names(self):
        polygon = Polygon.objects.get(id=1)
        field_names = []
        for field in self.field_list:
            field_names.append(polygon._meta.get_field(field).verbose_name)
        self.assertEqual(
            ['p name', 'price', 'information', 'provider'], field_names)

    def test_fields_null_acceptance(self):
        polygon = Polygon.objects.get(id=1)
        values = []
        for field in self.field_list:
            values.append(polygon._meta.get_field(field).null)
        self.assertEqual([False, False, False, False], values)
