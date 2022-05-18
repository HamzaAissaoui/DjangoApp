
from provider.models import Provider
from django.http import HttpResponseForbidden
from functools import wraps

default_message = 'You need to create a provider and add the "name" in headers'

def authorize(func):
    """Only providers are allowed to access"""
    @wraps(func)
    def inner(request, *args, **kwargs):
        name=request.headers.get('name', None)
        if Provider.objects.filter(name=name):
            returned_value = func(request, *args, **kwargs)
            return returned_value
        else:
            return HttpResponseForbidden(default_message)

    return inner

