from django.db import models
from django.utils.timezone import now

class Produit(models.Model):
    nom_produit = models.CharField(max_length=100)  # Nom du produit
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Prix par défaut
    default_description = models.TextField(blank=True, null=True)  # Description par défaut
    created_at = models.DateTimeField(default=now)  # Utiliser timezone.now comme valeur par défaut

    def __str__(self):
        return self.nom_produit

class Vendeur(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    nom_du_vendeur = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)  # Adresse e-mail
    Sexe = models.CharField(max_length=1, choices=GENDER_CHOICES)  # Sexe

    def __str__(self):
        return self.nom_du_vendeur

class Sale(models.Model):
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)  # Champ correct
    seller = models.ForeignKey('Vendeur', on_delete=models.CASCADE)
    description = models.TextField(default="Aucune description")
    license_plate = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produit} vendu par {self.seller}"

class Invoice(models.Model):
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number

class POS(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    connection_type = models.CharField(max_length=50, choices=[('Bluetooth', 'Bluetooth'), ('USB', 'USB')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_connected = models.BooleanField(default=False)

    def __str__(self):
        return self.name