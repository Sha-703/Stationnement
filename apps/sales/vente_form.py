from django import forms
from apps.sales.models import TypeEngin

class VenteForm(forms.Form):
    type_engin = forms.ModelChoiceField(queryset=TypeEngin.objects.all(), label="Type d'engin", required=True)
    description = forms.CharField(label="Description", widget=forms.Textarea, required=True)
    license_plate = forms.CharField(label="Numéro matricule", max_length=20, required=True)
