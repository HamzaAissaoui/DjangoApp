from provider import views
from django.urls import path

urlpatterns = [
    path('', views.get_all_providers),
    path('<int:id>', views.get_provider_by_id),
]