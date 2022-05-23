from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from provider.models import Provider
from techChallenge.decorators import authorize
from django.contrib.gis.geos import Polygon as Poly, Point
from .models import Polygon
from django.core.paginator import Paginator
from .helper import validate_create_data, INVALID_POLYGON_MESSAGE, check_polygon_existence, validate_update_data
from django.core.serializers import serialize
# Create your views here.


@require_GET
def get_polygons(request):
    lng = request.GET.get('lng', None)  # Default value None
    lat = request.GET.get('lat', None)
    fields = ['p_name', 'price', 'information', 'provider']
    if lng is None or lat is None:
        polygon_list = Polygon.objects.all()
    else:
        polygon_list = Polygon.objects.filter(information__covers=Point(
            float(lng), float(lat)))  # All polygons that contain the coordinates
        fields.remove('information')  # We don't return geojson for lat/lng get requests

    paginator = Paginator(polygon_list, 20)  # 20 Polygons per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    response = serialize('json', page_obj, fields=tuple(fields))
    return HttpResponse(response, content_type='application/json') if page_obj else HttpResponseNotFound('There are no polygons!')


@require_GET
def get_polygon_by_id(request, id):
    polygon = Polygon.objects.filter(id=id)
    response = serialize('json', polygon)
    return HttpResponse(response, content_type='application/json') if polygon else HttpResponseNotFound('Polygon does not exist!')


@require_POST
@authorize
def create_polygon(request):
    username = request.headers.get('name')
    provider = Provider.objects.get(name=username)

    # Returns either the data or an http error
    data = validate_create_data(request, provider=provider)
    if not isinstance(data, dict):
        return data  # HTTP error

    p_name = data['p_name']
    price = data['price']
    try:
        # Converted to valid polygon object
        information = Poly(data['coordinates'])
        p = Polygon(p_name=p_name, price=price,
                    information=information, provider=provider)
        p.save()
    except:
        return HttpResponseBadRequest(INVALID_POLYGON_MESSAGE)
    response = serialize('json', p)
    return HttpResponse(response, content_type='application/json')     


@require_http_methods(['DELETE'])
@authorize
def delete_polygon_by_id(request, id):
    check_polygon = check_polygon_existence(request, id)  # Returns either the data or an http error
    if not isinstance(check_polygon, tuple):
        return check_polygon  # HTTP error
    check_polygon[0].delete()
    return HttpResponse('Polygon Deleted successfully!')


@require_http_methods(['PUT'])
@authorize
def update_polygon_by_id(request, id):
    check_polygon = check_polygon_existence(request, id, update=True)
    if not isinstance(check_polygon, tuple):
        return check_polygon  # HTTP error

    polygon_query = check_polygon[0]
    old_polygon = check_polygon[1]
    data = validate_update_data(request, old_polygon)  # Validating Request

    if data['information'] is None:
        polygon_query.update(
            p_name=data['p_name'], price=data['price'])  # Polygon query
    else:
        try:
            information = Poly(data['coordinates'])
            polygon_query.update(
                p_name=data['p_name'], price=data['price'], information=information)
        except Exception as e:
            print(e)
            return HttpResponseBadRequest(INVALID_POLYGON_MESSAGE)

    for query in polygon_query:
        query.save()
    response = serialize('json', polygon_query)
    return HttpResponse(response, content_type='application/json')  
