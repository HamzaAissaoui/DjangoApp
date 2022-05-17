from django.http import HttpResponse, HttpResponseBadRequest
import json
from .models import Provider

def validate_create_data(request):
    if not request.body:
        return HttpResponseBadRequest('Name and Email are required')
    data = json.loads(request.body.decode('utf-8')) 

    name = data.get('name', "") 
    email = data.get('email', "") 
    data['phone_number'] = data.get('phone_number', "") 
    data['language'] = data.get('language', "")
    data['currency'] = data.get('currency', "")  

    if name=="" or email=="":
        return HttpResponseBadRequest('Name and Email are required')
    if Provider.objects.filter(name=name):
        return HttpResponse('Name already exists', status=409)
        
    return data