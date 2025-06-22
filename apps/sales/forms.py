from django import forms
from .models import Sale, Vendeur, Produit, POS

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['produit', 'seller', 'description', 'license_plate']  # Remplacez 'product' par 'produit'

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Définir le prix automatiquement en fonction du produit sélectionné
        if instance.produit:  # Utilisez 'produit' au lieu de 'product'
            instance.price = instance.produit.prix
        if commit:
            instance.save()
        return instance

class VendeurForm(forms.ModelForm):
    class Meta:
        model = Vendeur
        fields = ['nom_du_vendeur', 'email']

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom_produit', 'prix', 'default_description']

class POSForm(forms.ModelForm):
    class Meta:
        model = POS
        fields = ['name', 'vendeur']