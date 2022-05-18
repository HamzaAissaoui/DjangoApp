from django.template.loader import render_to_string
from django.http import HttpResponse

def index(request):
    context_dict = {
        'documentation': 'api/v1/'
    }
    template = render_to_string("home.html", context_dict)
    return HttpResponse(template)
    return HttpResponse('hi')