from django.contrib import admin
from .models import TypeEngin, Vendeur, Sale, Invoice, POS

@admin.register(TypeEngin)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('nom_type_engin', 'prix', 'default_description', 'created_at')
    search_fields = ('nom_type_engin',)

@admin.register(Vendeur)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('nom_du_vendeur', 'email')
    search_fields = ('nom_du_vendeur', 'email')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('type_engin', 'seller', 'description', 'license_plate', 'price', 'created_at')
    search_fields = ('type_engin__nom_type_engin', 'seller__store_name')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('sale', 'invoice_number', 'issued_at')
    search_fields = ('invoice_number',)

@admin.register(POS)
class POSAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendeur', 'created_at', 'updated_at')
    search_fields = ('name',)