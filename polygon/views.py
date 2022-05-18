from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from provider.models import Provider
from techChallenge.decorators import authorize
from django.contrib.gis.geos import Polygon as Poly, Point
from .models import Polygon
from django.core.paginator import Paginator
import json
from .helper import validate_create_data, invalid_polygon_message
# Create your views here.


@require_GET
@authorize
def get_all_polygons(request):
    polygon_list = Polygon.objects.all()
    paginator = Paginator(polygon_list, 20)
    page_number = request.GET.get('page', 0)
    page_obj = paginator.get_page(page_number)
    return HttpResponse(page_obj) if page_obj else HttpResponseNotFound('There are no polygons')


@require_POST
@authorize
def create_polygon(request):
    username = request.headers.get('name')
    data = validate_create_data(request, username=username)
    if not isinstance(data, dict):
        return data  # Http Error

    p_name = data['p_name']
    price = data['price']
    provider = Provider.objects.get(name=username)
    try:
        information = Poly(data['coordinates'])
        p = Polygon(p_name=p_name, price=price,
                    information=information, name=provider)
        p.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest(invalid_polygon_message)

    return HttpResponse('Polygon created successfully!')


# return HttpResponse(Polygon.objects.filter(information__covers=Point(30,0)))
#
