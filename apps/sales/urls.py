from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SalesListView, SalesDetailView, CreateSaleView, ValidateSaleView, LoginView, ProductListView, InvoiceDetailView,
    vendeur_list_view, vendeur_create_view, vendeur_update_view, vendeur_delete_view,
    produit_list_view, produit_create_view, produit_update_view, produit_delete_view,
    POSViewSet, POSCreateView, update_pos_status, pos_list_view
)

router = DefaultRouter()
router.register(r'pos', POSViewSet, basename='pos')

urlpatterns = [
    path('sales/', SalesListView.as_view(), name='sales-list'),
    path('sales/<int:pk>/', SalesDetailView.as_view(), name='sales-detail'),
    path('sales/create/', CreateSaleView.as_view(), name='create-sale'),
    path('sales/validate/<int:pk>/', ValidateSaleView.as_view(), name='validate-sale'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('sales/<int:sale_id>/invoice/', InvoiceDetailView.as_view(), name='invoice-detail'),

    # Routes pour les vendeurs
    path('vendeurs/', vendeur_list_view, name='vendeur_list'),
    path('vendeurs/ajouter/', vendeur_create_view, name='vendeur_create'),
    path('vendeurs/modifier/<int:pk>/', vendeur_update_view, name='vendeur_update'),
    path('vendeurs/supprimer/<int:pk>/', vendeur_delete_view, name='vendeur_delete'),

    # Routes pour les produits
    path('produits/', produit_list_view, name='produit_list'),
    path('produits/ajouter/', produit_create_view, name='produit_create'),
    path('produits/modifier/<int:pk>/', produit_update_view, name='produit_update'),
    path('produits/supprimer/<int:pk>/', produit_delete_view, name='produit_delete'),

    path('pos/add/', POSCreateView.as_view(), name='add_pos'),
    path('pos/<int:pos_id>/update-status/', update_pos_status, name='update_pos_status'),
    path('pos/', pos_list_view, name='pos_list'),

    path('', include(router.urls)),
]