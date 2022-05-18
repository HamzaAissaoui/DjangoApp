from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from provider.models import Provider
from techChallenge.decorators import authorize
# Create your views here.

@authorize
def get_all_polygons(request):
    name = request.headers.get('Name', None)
    #Getting polygon from database here