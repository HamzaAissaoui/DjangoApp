from . import views
from django.urls import path

urlpatterns = [
    path('', views.get_all_polygons),
    path('create', views.create_polygon),
]            
