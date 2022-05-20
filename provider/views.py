from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.http import HttpResponse, HttpResponseNotFound
from django.core.paginator import Paginator
from ratelimit.decorators import ratelimit
from .helper import validate_create_data, validate_update_data
from .models import Provider


@require_GET
def get_all_providers(request):
    provider_list = Provider.objects.all()
    paginator = Paginator(provider_list, 20)  # Show 20 providers per page.
    page_number = request.GET.get('page', 0)
    page_obj = paginator.get_page(page_number)
    return HttpResponse(page_obj) if page_obj else HttpResponseNotFound('There are no providers')


@require_GET
def get_provider_by_id(request, id=None):
    p = Provider.objects.filter(id=id)
    return HttpResponse(p) if p else HttpResponseNotFound('Provider does not exist')


@require_POST
@ratelimit(key='ip', rate='5/m')  # to avoid spamming
def create_provider(request):
    data = validate_create_data(request)
    if not isinstance(data, dict):
        return data  # Http Error

    p = Provider(
        name=data['name'], email=data['email'], phone_number=data['phone_number'],
        language=data['language'], currency=data['currency']
    )

    p.save()
    return HttpResponse(p, status=201)


@require_http_methods(['DELETE'])
def delete_provider_by_id(request, id):
    p = Provider.objects.filter(id=id)
    if not p:
        return HttpResponseNotFound('Provider does not exist!')
    p.delete()
    return HttpResponse('Provider Deleted successfully!')


@require_http_methods(['PUT'])
def update_provider_by_id(request, id):
    provider_query = Provider.objects.filter(id=id)
    if not provider_query:
        return HttpResponseNotFound('Provider does not exist')

    data = validate_update_data(request, provider_query.first())
    if not isinstance(data, dict):
        return data  # Http Error

    provider_query.update(name=data['name'], email=data['email'],
                          phone_number=data['phone_number'], language=data['language'], currency=data['currency'])
    for query in provider_query:
        query.save()
    return HttpResponse(provider_query)
