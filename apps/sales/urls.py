from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SalesListView, SalesDetailView, CreateSaleView, ValidateSaleView, LoginView, InvoiceDetailView,
    vendeur_list_view, vendeur_create_view, vendeur_update_view, vendeur_delete_view,
    POSViewSet, POSCreateView, POSUpdateView, update_pos_status, pos_list_view,
    identification_vendeur, effectuer_vente, voir_facture, previsualiser_facture, enregistrer_vente_apres_impression,
    pos_delete_view, VendeurLoginAPIView,
    rapport_vente_vendeur, accueil_vendeur, historique_vente, logout_vendeur, historique_vendeur,
    rapport_vente_vendeur_print, login_view, enregistrer_vente_apres_impression, logout_utilisateur,
    TypeEnginListView, TypeEnginCreateView, TypeEnginUpdateView, TypeEnginDeleteView,
    ZoneListView, ZoneCreateView,
    rapport_vente_zone
)

router = DefaultRouter()
router.register(r'pos', POSViewSet, basename='pos')

urlpatterns = [
    path('sales/', SalesListView.as_view(), name='sales-list'),
    path('sales/<int:pk>/', SalesDetailView.as_view(), name='sales-detail'),
    path('sales/create/', CreateSaleView.as_view(), name='create-sale'),
    path('sales/validate/<int:pk>/', ValidateSaleView.as_view(), name='validate-sale'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('sales/<int:sale_id>/invoice/', InvoiceDetailView.as_view(), name='invoice-detail'),

    # Routes pour les vendeurs
    path('vendeurs/', vendeur_list_view, name='vendeur_list'),
    path('vendeurs/ajouter/', vendeur_create_view, name='vendeur_create'),
    path('vendeurs/modifier/<int:pk>/', vendeur_update_view, name='vendeur_update'),
    path('vendeurs/supprimer/<int:pk>/', vendeur_delete_view, name='vendeur_delete'),

    path('pos/delete/<int:pk>/', pos_delete_view, name='delete_pos'),
    path('pos/add/', POSCreateView.as_view(), name='add_pos'),
    path('pos/<int:pos_id>/update-status/', update_pos_status, name='update_pos_status'),
    path('pos/', pos_list_view, name='pos_list'),
    path('pos/modifier/<int:pk>/', POSUpdateView.as_view(), name='update_pos'),

    # Routes POS pour vente rapide
    path('vente/identification/', identification_vendeur, name='identification_vendeur'),
    path('vente/creer/', effectuer_vente, name='effectuer_vente'),
    path('vente/facture/<int:pk>/', voir_facture, name='voir_facture'),
    path('vente/previsualiser-facture/', previsualiser_facture, name='previsualiser_facture'),
    path('vente/enregistrer-apres-impression/', enregistrer_vente_apres_impression, name='enregistrer_vente_apres_impression'),

    path('api/vendeur/login/', VendeurLoginAPIView.as_view(), name='vendeur_login_api'),

    path('rapport-vendeur/', rapport_vente_vendeur, name='rapport_vente_vendeur'),
    path('accueil-vendeur/', accueil_vendeur, name='accueil_vendeur'),
    path('historique-vente/', historique_vente, name='historique_vente'),
    path('logout-vendeur/', logout_vendeur, name='logout_vendeur'),
    path('historique-vendeur/<int:vendeur_id>/', historique_vendeur, name='historique_vendeur'),
    path('rapport-vendeur/print/', rapport_vente_vendeur_print, name='rapport_vente_vendeur_print'),
    path('rapport-vendeur/print/<int:vendeur_id>/', rapport_vente_vendeur_print, name='rapport_vente_vendeur_print'),

    path('', include(router.urls)),
    path('login/', login_view, name='login'),
    path('logout/', logout_utilisateur, name='logout'),

    # Routes pour les types d'engin
    path('types-engin/', TypeEnginListView.as_view(), name='type_engin_list'),
    path('types-engin/ajouter/', TypeEnginCreateView.as_view(), name='type_engin_create'),
    path('types-engin/modifier/<int:pk>/', TypeEnginUpdateView.as_view(), name='type_engin_update'),
    path('types-engin/supprimer/<int:pk>/', TypeEnginDeleteView.as_view(), name='type_engin_delete'),

    # Routes pour les zones
    path('zones/', ZoneListView.as_view(), name='zone_list'),
    path('zones/ajouter/', ZoneCreateView.as_view(), name='zone_create'),

    path('rapport-zone/', rapport_vente_zone, name='rapport_vente_zone'),
]