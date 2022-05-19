from . import views
from django.urls import path

urlpatterns = [
    path('', views.get_polygons),
    path('create', views.create_polygon),
    path('<int:id>', views.get_polygon_by_id),
    path('<int:id>/delete', views.delete_polygon_by_id),
    path('<int:id>/update', views.update_polygon_by_id),
]            
