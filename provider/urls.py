from . import views
from django.urls import path

urlpatterns = [
    path('', views.get_all_providers, name='get-providers'),
    path('<int:id>', views.get_provider_by_id, name='get-provider-by-id'),
    path('create', views.create_provider, name='create-provider'),
    path('<int:id>/delete', views.delete_provider_by_id, name='delete-provider'),
    path('<int:id>/update', views.update_provider_by_id, name='update-provider'),
]
