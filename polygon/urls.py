from . import views
from django.urls import path

urlpatterns = [
    path('', views.get_polygons, name='get-polygons'),
    path('create', views.create_polygon, name='create-polygon'),
    path('<int:id>', views.get_polygon_by_id, name='get-polygon-by-id'),
    path('<int:id>/delete', views.delete_polygon_by_id, name='delete-polygon'),
    path('<int:id>/update', views.update_polygon_by_id, name='update-polygon'),
]
