from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Produit, Sale, Vendeur, POS  # Importez votre modèle Vendeur
from .serializers import ProductSerializer, SaleSerializer, InvoiceSerializer, POSSerializer
from .forms import VendeurForm, ProduitForm, POSForm

User = get_user_model()

class ProductViewSet(ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProductSerializer

class ProductListView(ListAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProductSerializer

class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SalesListView(ListAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class SalesDetailView(RetrieveAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class CreateSaleView(APIView):
    def post(self, request):
        produit_id = request.data.get('produit_id')
        vendeur_id = request.data.get('vendeur_id')
        description = request.data.get('description')
        license_plate = request.data.get('license_plate')

        try:
            produit = Produit.objects.get(id=produit_id)
            vendeur = Vendeur.objects.get(id=vendeur_id)
            sale = Sale.objects.create(
                produit=produit,
                seller=vendeur,
                description=description,
                license_plate=license_plate,
                price=produit.prix
            )
            return Response({"message": "Vente créée avec succès", "sale_id": sale.id}, status=status.HTTP_201_CREATED)
        except Produit.DoesNotExist:
            return Response({"error": "Produit introuvable"}, status=status.HTTP_404_NOT_FOUND)
        except Vendeur.DoesNotExist:
            return Response({"error": "Vendeur introuvable"}, status=status.HTTP_404_NOT_FOUND)

class ValidateSaleView(APIView):
    def post(self, request, pk):
        # Ajoutez ici la logique pour valider une vente
        return Response({"message": "Vente validée avec succès"}, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        nom_du_vendeur = request.data.get('nom_du_vendeur')

        # Vérifiez si un vendeur avec cet email et ce nom existe
        try:
            vendeur = Vendeur.objects.get(email=email, nom_du_vendeur=nom_du_vendeur)
            return Response({"message": "Connexion réussie", "vendeur_id": vendeur.id}, status=status.HTTP_200_OK)
        except Vendeur.DoesNotExist:
            return Response({"error": "Nom ou email invalide"}, status=status.HTTP_401_UNAUTHORIZED)

class InvoiceDetailView(APIView):
    def get(self, request, sale_id):
        try:
            sale = Sale.objects.get(id=sale_id)
            serializer = InvoiceSerializer(sale)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Sale.DoesNotExist:
            return Response({"error": "Vente introuvable"}, status=status.HTTP_404_NOT_FOUND)

class POSViewSet(viewsets.ModelViewSet):
    queryset = POS.objects.all()
    serializer_class = POSSerializer

class POSCreateView(CreateView):
    model = POS
    form_class = POSForm
    template_name = 'pos_form.html'
    success_url = reverse_lazy('dashboard')

@api_view(['POST'])
def update_pos_status(request, pos_id):
    try:
        pos = POS.objects.get(id=pos_id)
        pos.is_connected = request.data.get('is_connected', False)
        pos.save()
        return Response({'message': 'État du POS mis à jour avec succès.'}, status=status.HTTP_200_OK)
    except POS.DoesNotExist:
        return Response({'error': 'POS non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Liste des vendeurs
def vendeur_list_view(request):
    vendeurs = Vendeur.objects.all()
    return render(request, 'vendeurs_list.html', {'vendeurs': vendeurs})

# Ajouter un vendeur
def vendeur_create_view(request):
    if request.method == 'POST':
        form = VendeurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vendeur_list')
    else:
        form = VendeurForm()
    return render(request, 'vendeur_form.html', {'form': form})

# Modifier un vendeur
def vendeur_update_view(request, pk):
    vendeur = get_object_or_404(Vendeur, pk=pk)
    if request.method == 'POST':
        form = VendeurForm(request.POST, instance=vendeur)
        if form.is_valid():
            form.save()
            return redirect('vendeur_list')
    else:
        form = VendeurForm(instance=vendeur)
    return render(request, 'vendeur_form.html', {'form': form})

# Supprimer un vendeur
def vendeur_delete_view(request, pk):
    vendeur = get_object_or_404(Vendeur, pk=pk)
    if request.method == 'POST':
        vendeur.delete()
        return redirect('vendeur_list')
    return render(request, 'vendeur_confirm_delete.html', {'vendeur': vendeur})

# Liste des produits
def produit_list_view(request):
    produits = Produit.objects.all()
    return render(request, 'produits_list.html', {'produits': produits})

# Ajouter un produit
def produit_create_view(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produit_list')
    else:
        form = ProduitForm()
    return render(request, 'produit_form.html', {'form': form})

# Modifier un produit
def produit_update_view(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('produit_list')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'produit_form.html', {'form': form})

# Supprimer un produit
def produit_delete_view(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        produit.delete()
        return redirect('produit_list')
    return render(request, 'produit_confirm_delete.html', {'produit': produit})

def pos_list_view(request):
    pos_list = POS.objects.all()
    return render(request, 'pos_list.html', {'pos_list': pos_list})
