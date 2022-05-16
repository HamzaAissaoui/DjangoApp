from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse
from .models import Provider
# Create your views here.

@require_GET
def get_all_providers(request):
    return HttpResponse(Provider.objects.all())

@require_GET
def get_provider_by_id(request, id):
    return HttpResponse(Provider.objects.filter(id=id))