from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
import json
from .models import Polygon
INVALID_POLYGON_MESSAGE = """Invalid polygon:
                            - coordinates should be in the form [ [ x , y ] , [ x , y ] , [ x , y ] , [ x , y ] ]
                            - first and last point need to have the same coordinates
                            - there should be at least 4 points"""


def validate_create_data(request, provider):
    if not request.body:
        return HttpResponseBadRequest('No data was received')

    data = json.loads(request.body.decode('utf-8'))
    p_name = data.get('p_name', None)
    price = data.get('price', None)
    information = data.get('coordinates', None)

    if not p_name or not price or not information:
        return HttpResponseBadRequest('p_name and price and coordinates are required')

    if Polygon.objects.filter(p_name=p_name, provider=provider):
        return HttpResponse('polygon already exists for this user', status=409)

    return data


def check_polygon_existence(request, id, update=False):
    if update:
        if not request.body:
            return HttpResponseBadRequest('No data was received')
    username = request.headers.get('name')

    polygon_query = Polygon.objects.filter(id=id)
    if not polygon_query:
        return HttpResponseNotFound('Polygon does not exist!')

    polygon = polygon_query.first()
    if polygon.provider.name != username:
        return HttpResponseForbidden('You are not the creator of this polygon!')

    return polygon_query, polygon


def validate_update_data(request, polygon):
    if not request.body:
        return HttpResponseBadRequest('No data was received')

    data = json.loads(request.body.decode('utf-8'))
    data['p_name'] = data.get('p_name', polygon.p_name)
    data['price'] = data.get('price', polygon.price)
    data['information'] = data.get('coordinates', None)

    return data
