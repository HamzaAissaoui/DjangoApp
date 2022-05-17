from provider import views
from django.urls import path

urlpatterns = [
    path('', views.get_all_providers),
    path('<int:id>', views.get_provider_by_id),
    path('create', views.create_provider),
    path('<int:id>/delete', views.delete_provider_by_id),
    path('<int:id>/update', views.update_provider_by_id),

]