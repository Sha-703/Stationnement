from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('sales/', views.sales_list_view, name='sales_list'),
    path('statistics/', views.dashboard_statistics, name='dashboard_statistics'),
    path('export_sales_csv/', views.export_sales_csv, name='export_sales_csv'),
    path('', include('apps.dashboard.urls_ventes')),
]
