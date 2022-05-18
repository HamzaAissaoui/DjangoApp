from django.http import HttpResponse, HttpResponseBadRequest
import json
from .models import Polygon
invalid_polygon_message = """Invalid polygon:
                            - coordinates should be in the form [ [ x , y ] , [ x , y ] , [ x , y ] , [ x , y ] ]
                            - first and last point need to have the same coordinates
                            - there should be at least 4 points"""


def validate_create_data(request, username):
    if not request.body:
        return HttpResponseBadRequest('No data was received')

    data = json.loads(request.body.decode('utf-8'))
    p_name = data.get('p_name', None)
    price = data.get('price', None)
    information = data.get('coordinates', None)

    if not p_name or not price or not information:
        return HttpResponseBadRequest('p_name and price and coordinates are required')

    if Polygon.objects.filter(p_name=p_name, name=username):
        return HttpResponse('polygon already exists for this user', status=409)

    return data
