from django import forms
from apps.sales.models import Produit

class VenteForm(forms.Form):
    produit = forms.ModelChoiceField(queryset=Produit.objects.all(), label="Produit", required=True)
    description = forms.CharField(label="Description", widget=forms.Textarea, required=True)
    license_plate = forms.CharField(label="Numéro matricule", max_length=20, required=True)
