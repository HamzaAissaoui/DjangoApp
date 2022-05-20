from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from provider.models import Provider
from techChallenge.decorators import authorize
from django.contrib.gis.geos import Polygon as Poly, Point
from .models import Polygon
from django.core.paginator import Paginator
from .helper import validate_create_data, INVALID_POLYGON_MESSAGE, check_polygon_existence, validate_update_data
# Create your views here.


@require_GET
@authorize
def get_polygons(request):
    lng = request.GET.get('lng', None)
    lat = request.GET.get('lat', None)
    if lng is None or lat is None:
        polygon_list = Polygon.objects.all()
    else:
        polygon_list = Polygon.objects.filter(information__covers=Point(float(lng), float(lat)))
    paginator = Paginator(polygon_list, 20)
    page_number = request.GET.get('page', 0)
    page_obj = paginator.get_page(page_number)
    return HttpResponse(page_obj) if page_obj else HttpResponseNotFound('There are no polygons')


@require_GET
@authorize
def get_polygon_by_id(request, id):
    polygon = Polygon.objects.filter(id=id).first()
    return HttpResponse(polygon) if polygon else HttpResponseNotFound('Polygon does not exist')


@require_POST
@authorize
def create_polygon(request):
    username = request.headers.get('name')
    provider = Provider.objects.get(name=username)
    data = validate_create_data(request, provider=provider)
    if not isinstance(data, dict):
        return data  # Http Error

    p_name = data['p_name']
    price = data['price']
    try:
        information = Poly(data['coordinates'])
        p = Polygon(p_name=p_name, price=price,
                    information=information, provider=provider)
        p.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest(INVALID_POLYGON_MESSAGE)

    return HttpResponse('Polygon created successfully!')


@require_http_methods(['DELETE'])
@authorize
def delete_polygon_by_id(request, id):
    check_polygon = check_polygon_existence(request, id)
    if not isinstance(check_polygon, tuple):
        return check_polygon  # Http Error
    check_polygon[0].delete()
    return HttpResponse('Polygon Deleted successfully!')


@require_http_methods(['PUT'])
@authorize
def update_polygon_by_id(request, id):
    check_polygon = check_polygon_existence(request, id, update=True)
    if not isinstance(check_polygon, tuple):
        return check_polygon  # Http Error

    data = validate_update_data(request, check_polygon[1])  # Sending polygon object
    if data['information'] is None:
        check_polygon[0].update(p_name=data['p_name'], price=data['price'])  # Polygon query
    else:
        try:
            information = Poly(data['coordinates'])
            check_polygon[0].update(p_name=data['p_name'], price=data['price'], information=information)

        except Exception as e:
            print(e)
            return HttpResponseBadRequest(INVALID_POLYGON_MESSAGE)

    for query in check_polygon[0]:
        query.save()
    return HttpResponse(check_polygon[0])
