from django.template.loader import render_to_string
from django.http import HttpResponse


def index(request):
    template = render_to_string("home.html")
    return HttpResponse(template)
