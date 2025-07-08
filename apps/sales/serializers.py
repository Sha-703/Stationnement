from rest_framework import serializers
from .models import TypeEngin, Sale, Vendeur, POS, Invoice

class TypeEnginSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeEngin
        fields = ['id', 'nom_type_engin', 'prix', 'default_description', 'created_at']

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'type_engin', 'seller', 'description', 'license_plate', 'price', 'created_at']

class InvoiceSerializer(serializers.ModelSerializer):
    type_engin_nom = serializers.CharField(source='type_engin.nom_type_engin')
    type_engin_prix = serializers.DecimalField(source='type_engin.prix', max_digits=10, decimal_places=2)
    vendeur_nom = serializers.CharField(source='seller.nom_du_vendeur')

    class Meta:
        model = Sale
        fields = ['id', 'type_engin_nom', 'type_engin_prix', 'vendeur_nom', 'description', 'license_plate', 'price', 'created_at']

class POSSerializer(serializers.ModelSerializer):
    class Meta:
        model = POS
        fields = '__all__'