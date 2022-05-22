from django.test import TestCase
from provider.models import Provider
from django.urls import reverse
# Create your tests here.


class ProviderViewTest(TestCase):
    field_list = ['name', 'email', 'phone_number', 'language', 'currency']

    def setUp(self):
        # Create 13 providers for pagination tests
        number_of_providers = 22

        for provider_id in range(number_of_providers):
            Provider.objects.create(
                name=f'Hamza {provider_id}',
                email=f'test{provider_id}@gmail.com',
                phone_number='4084132222',
                language='French',
                currency='EUR'
            )

    def test_message_no_existing_providers(self):
        Provider.objects.all().delete()
        response = self.client.get(reverse('get-providers'))
        self.assertRaisesMessage(response, 'There are no providers')
        self.assertEqual(response.status_code, 404)

    def test_pagination_is_twenty(self):
        response = self.client.get(reverse('get-providers'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 20)

    def test_list_all_providers(self):
        # Get second page and confirm it has (exactly) remaining 2 items
        response = self.client.get(reverse('get-providers'), data={'page':2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)