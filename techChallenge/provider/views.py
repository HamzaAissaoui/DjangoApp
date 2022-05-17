from locale import currency
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse
from .models import Provider
from ratelimit.decorators import ratelimit
from .helper import validate_create_data
from django.core.paginator import Paginator
# Create your views here.

@require_GET
def get_all_providers(request):
    provider_list = Provider.objects.all()
    paginator = Paginator(provider_list, 20) # Show 20 providers per page.

    page_number = request.GET.get('page', 0)
    page_obj = paginator.get_page(page_number)
    return HttpResponse(page_obj)

@require_GET
def get_provider_by_id(request, id):
    return HttpResponse(Provider.objects.filter(id=id))

@require_POST
@ratelimit(key='ip', rate='10/m')
def create_provider(request):

    data = validate_create_data(request)
    if not isinstance(data, dict): return data
    
    p = Provider(
                name=data['name'], email=data['email'], phone_number=data['phone_number'], 
                language=data['language'], currency=data['currency']
            )
    p.save()
    return HttpResponse(p, status=201)
