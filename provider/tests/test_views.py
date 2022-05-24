from django.test import TestCase
from provider.models import Provider
from django.urls import reverse
from django.utils.encoding import force_text

# Create your tests here.


class ProviderViewGetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 22 providers for pagination tests
        number_of_providers = 22
        for provider_id in range(number_of_providers):
            Provider.objects.create(
                name=f'Hamza {provider_id}',
                email=f'test{provider_id}@gmail.com',
                phone_number='4084132222',
                language='French',
                currency='EUR'
            )

    def test_pagination_is_twenty(self):
        response = self.client.get(reverse('get-providers'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 20)

    def test_list_all_providers(self):
        # Get second page and confirm it has (exactly) remaining 2 items
        response = self.client.get(reverse('get-providers'), data={'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_get_provider_by_id_non_existant(self):
        inexistant_id = 25
        response = self.client.get(
            reverse('get-provider-by-id',  kwargs={'id': inexistant_id}))
        self.assertEqual(
            force_text(response.content), 'Provider does not exist!')

    def test_get_provider_by_id_correct(self):
        existant_id = 3
        response = self.client.get(
            reverse('get-provider-by-id',  kwargs={'id': existant_id}))
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json(), [{'model': 'provider.provider', 'pk': 3, 'fields': {
                         'name': 'Hamza 0', 'email': 'test0@gmail.com', 'phone_number': '4084132222',
                         'language': 'French', 'currency': 'EUR'}}])

    # def test_message_no_existing_providers(self):
    #     Provider.objects.all().delete()
    #     response = self.client.get(reverse('get-providers'))
    #     self.assertRaisesMessage(response, 'There are no providers')
    #     self.assertEqual(response.status_code, 404)


class ProviderViewDeleteTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 1 provider for delete tests
        Provider.objects.create(
            name=f'Hamza 23',
            email=f'test23@gmail.com',
            phone_number='4084132222',
            language='French',
            currency='EUR'
        )

    def test_delete_non_existant_id(self):
        inexistant_id = 24
        response = self.client.delete(
            reverse('delete-provider',  kwargs={'id': inexistant_id}))
        self.assertEqual(
            force_text(response.content), 'Provider does not exist!')

    def test_delete_correct_id(self):
        existant_id = 2
        response = self.client.delete(
            reverse('delete-provider',  kwargs={'id': existant_id}))
        self.assertEqual(
            force_text(response.content), 'Provider Deleted successfully!')


class ProviderViewUpdateTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Provider.objects.create(
            name=f'Hamza 24',
            email=f'test23@gmail.com',
            phone_number='4084132222',
            language='French',
            currency='EUR'
        )
        Provider.objects.create(
            name=f'Hamza 0',
            email=f'test23@gmail.com',
            phone_number='4084132222',
            language='French',
            currency='EUR'
        )

    def test_update_non_existant_id(self):
        inexistant_id = 24
        response = self.client.put(
            reverse('update-provider',  kwargs={'id': inexistant_id}))
        self.assertEqual(
            force_text(response.content), 'Provider does not exist!')

    def test_update_without_sending_data(self):
        response = self.client.put(
            reverse('update-provider',  kwargs={'id': 25}))
        self.assertEqual(
            force_text(response.content), 'No data was received')

    def test_update_with_existing_name(self):
        response = self.client.put(
            reverse('update-provider',  kwargs={'id': 25}), {'name': 'Hamza 0'}, content_type='application/json')
        self.assertEqual(
            force_text(response.content), 'Name already exists, please use another one!')

    def test_update_with_correct(self):
        response = self.client.put(
            reverse('update-provider',  kwargs={'id': 25}), {'name': 'Hamza 26'}, content_type='application/json')
        self.assertEqual(response.json(), [{"model": "provider.provider", "pk": 25, "fields": {
                         "name": "Hamza 26", "email": "test23@gmail.com", "phone_number": "4084132222",
                         "language": "French", "currency": "EUR"}}])
