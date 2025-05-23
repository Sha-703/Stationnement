from rest_framework import serializers
from .models import Produit, Sale, POS

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ['id', 'nom_produit', 'prix', 'default_description']

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'produit', 'seller', 'description', 'license_plate', 'price', 'created_at']

class InvoiceSerializer(serializers.ModelSerializer):
    produit_nom = serializers.CharField(source='produit.nom_produit')
    produit_prix = serializers.DecimalField(source='produit.prix', max_digits=10, decimal_places=2)
    vendeur_nom = serializers.CharField(source='seller.nom_du_vendeur')

    class Meta:
        model = Sale
        fields = ['id', 'produit_nom', 'produit_prix', 'vendeur_nom', 'description', 'license_plate', 'price', 'created_at']

class POSSerializer(serializers.ModelSerializer):
    class Meta:
        model = POS
        fields = '__all__'