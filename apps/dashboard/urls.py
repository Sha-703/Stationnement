from django.urls import path, include
from . import views
from apps.sales.views import rapport_vente_vendeur

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('sales/', rapport_vente_vendeur, name='sales_list'),
    path('statistics/', views.dashboard_statistics, name='dashboard_statistics'),
    path('export_sales_csv/', views.export_sales_csv, name='export_sales_csv'),
    path('', include('apps.dashboard.urls_ventes')),
]
