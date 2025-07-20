from django import forms
from .models import Sale, Vendeur, TypeEngin, POS, Zone

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['type_engin', 'seller', 'description', 'license_plate']  # Remplacez 'product' par 'type_engin'

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Définir le prix automatiquement en fonction du produit sélectionné
        if instance.type_engin:  # Utilisez 'type_engin' au lieu de 'product'
            instance.price = instance.type_engin.prix
        if commit:
            instance.save()
        return instance

class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['nom', 'description']

class VendeurForm(forms.ModelForm):
    class Meta:
        model = Vendeur
        fields = ['nom_du_vendeur', 'email', 'zone']

class TypeEnginForm(forms.ModelForm):
    class Meta:
        model = TypeEngin
        fields = ['nom_type_engin', 'prix', 'default_description']

class POSForm(forms.ModelForm):
    class Meta:
        model = POS
        fields = ['name', 'vendeur']