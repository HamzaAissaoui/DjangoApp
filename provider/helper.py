from django.http import HttpResponse, HttpResponseBadRequest
import json
from .models import Provider


def validate_create_data(request):
    if not request.body:
        return HttpResponseBadRequest('No data was received')

    data = json.loads(request.body.decode('utf-8'))
    name = data.get('name', "")
    email = data.get('email', "")
    data['phone_number'] = data.get('phone_number', "") #it's not mandatory
    data['language'] = data.get('language', "")
    data['currency'] = data.get('currency', "")

    if not name or not email:
        return HttpResponseBadRequest('Name and Email are required')

    if Provider.objects.filter(name=name):
        return HttpResponse('Name already exists', status=409)

    return data


def validate_update_data(request, provider):
    if not request.body:
        return HttpResponseBadRequest('No data was received')

    data = json.loads(request.body.decode('utf-8'))
    data['name'] = data.get('name', provider.name)
    data['email'] = data.get('email', provider.email)
    data['phone_number'] = data.get('phone_number', provider.phone_number)
    data['language'] = data.get('language', provider.language)
    data['currency'] = data.get('currency', provider.currency)
    return data
