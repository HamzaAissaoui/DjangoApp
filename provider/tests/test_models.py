from django.test import TestCase
from provider.models import Provider
# Create your tests here.


class ProviderModelTest(TestCase):
    field_list = ['name', 'email', 'phone_number', 'language', 'currency']

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Provider.objects.create(name='hamza', email='test@gmail.com', phone_number='4084132222',
                                language='French', currency='EUR')

    def test_name_uniqueness(self):
        provider = Provider.objects.get(id=1)
        unique = provider._meta.get_field('name').unique
        self.assertTrue(unique)

    def test_provider_object_string(self):
        provider = Provider.objects.get(id=1)
        expected_object_name = f"\n- Provider({provider.name!r}, {provider.email!r}, {provider.phone_number!r}, \
                {provider.language!r}, {provider.currency!r})"
        self.assertEqual(str(provider), expected_object_name)

    def test_fields_max_length(self):
        provider = Provider.objects.get(id=1)
        max_lengths = []
        for field in self.field_list:
            max_lengths.append(provider._meta.get_field(field).max_length)
        self.assertEqual([128, 128, 15, 30, 30], max_lengths)

    def test_fields_field_names(self):
        provider = Provider.objects.get(id=1)
        field_names = []
        for field in self.field_list:
            field_names.append(provider._meta.get_field(field).verbose_name)
        self.assertEqual(['name', 'email', 'phone number',
                         'language', 'currency'], field_names)

    def test_fields_null_acceptance(self):
        provider = Provider.objects.get(id=1)
        values = []
        for field in self.field_list:
            values.append(provider._meta.get_field(field).null)
        self.assertEqual([False, False, True, True, True], values)
