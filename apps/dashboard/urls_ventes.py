from django.urls import path
from .views_ventes import ventes_list_view

urlpatterns = [
    path('ventes/', ventes_list_view, name='ventes_list'),
]
