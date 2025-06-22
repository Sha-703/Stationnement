from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Produit, Sale, Vendeur, POS, Invoice  # Ajout de Invoice à l'import
from .serializers import ProductSerializer, SaleSerializer, InvoiceSerializer, POSSerializer
from .forms import VendeurForm, ProduitForm, POSForm
from .vente_form import VenteForm
import qrcode
import base64
from io import BytesIO
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.utils import timezone
from datetime import timedelta
from django.template import RequestContext
from django.db.models import Sum

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
            # Génération du QR code
            import qrcode
            import base64
            from io import BytesIO
            qr = qrcode.QRCode(box_size=3, border=2)
            qr.add_data(f"Facture N° {sale.id} | {sale.license_plate}")
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
            data = serializer.data
            data['qr_code_base64'] = qr_code_base64
            # Ajout du mail vendeur
            data['vendeur_email'] = sale.seller.email
            return Response(data, status=status.HTTP_200_OK)
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

class VendeurIdentificationForm(forms.Form):
    nom_du_vendeur = forms.CharField(label="Nom du vendeur", max_length=100)
    email = forms.EmailField(label="Email", max_length=255)

@csrf_exempt
def identification_vendeur(request):
    # Si la requête vient de l'app mobile (JSON)
    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        import json
        data = json.loads(request.body)
        nom = data.get('nom_du_vendeur')
        email = data.get('email')
        try:
            vendeur = Vendeur.objects.get(nom_du_vendeur=nom, email=email)
            return JsonResponse({'vendeur_id': vendeur.id, 'message': 'ok'})
        except Vendeur.DoesNotExist:
            return JsonResponse({'error': 'Nom ou email invalide'}, status=401)
    # Sinon, comportement classique (formulaire HTML)
    message = None
    if request.method == 'POST':
        form = VendeurIdentificationForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom_du_vendeur']
            email = form.cleaned_data['email']
            try:
                vendeur = Vendeur.objects.get(nom_du_vendeur=nom, email=email)
                request.session['vendeur_id'] = vendeur.id
                return redirect('accueil_vendeur')
            except Vendeur.DoesNotExist:
                message = "Aucun vendeur trouvé avec ce nom et cet email. Veuillez réessayer."
        else:
            message = "Veuillez remplir correctement le formulaire."
    else:
        form = VendeurIdentificationForm()
    return render(request, 'identification_vendeur.html', {'form': form, 'message': message})

@csrf_exempt
def effectuer_vente(request):
    vendeur_id = request.session.get('vendeur_id')
    if not vendeur_id:
        return redirect('identification_vendeur')
    vendeur = Vendeur.objects.get(id=vendeur_id)
    pos = POS.objects.first()
    if request.method == 'POST':
        form = VenteForm(request.POST)
        if form.is_valid():
            produit = form.cleaned_data['produit']
            description = form.cleaned_data['description']
            license_plate = form.cleaned_data['license_plate']
            price = produit.prix
            sale = Sale.objects.create(
                produit=produit,
                seller=vendeur,
                description=description,
                license_plate=license_plate,
                price=price,
                source='POS'
            )
            numero_facture = f"FCT-{sale.id}-{sale.created_at.strftime('%Y%m%d%H%M%S')}"
            facture = Invoice.objects.create(sale=sale, invoice_number=numero_facture)
            return redirect('voir_facture', pk=facture.pk)
    else:
        form = VenteForm()
    return render(request, 'effectuer_vente.html', {'form': form, 'vendeur': vendeur, 'pos': pos})

def voir_facture(request, pk):
    facture = Invoice.objects.get(pk=pk)
    sale = facture.sale
    # Générer un QR code avec toutes les infos de la vente
    qr = qrcode.QRCode(box_size=3, border=2)
    qr_data = f"Facture: {facture.invoice_number}\nDate: {sale.created_at.strftime('%d/%m/%Y %H:%M')}\nVendeur: {sale.seller.nom_du_vendeur}\nProduit: {sale.produit.nom_produit}\nImmatriculation: {sale.license_plate}\nPrix: {sale.price} Fc\nDescription: {sale.description}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    html = render_to_string('facture.html', {
        'facture': facture,
        'vente': sale,
        'qr_code_base64': qr_code_base64
    })
    return HttpResponse(html)

def pos_delete_view(request, pk):
    pos = get_object_or_404(POS, pk=pk)
    if request.method == 'POST':
        pos.delete()
        return redirect('pos_list')
    return render(request, 'pos_confirm_delete.html', {'pos': pos})

class VendeurLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        nom_du_vendeur = request.data.get('nom_du_vendeur')
        try:
            vendeur = Vendeur.objects.get(email=email, nom_du_vendeur=nom_du_vendeur)
            return Response({'vendeur_id': vendeur.id, 'message': 'ok'}, status=status.HTTP_200_OK)
        except Vendeur.DoesNotExist:
            return Response({'error': 'Nom ou email invalide'}, status=status.HTTP_401_UNAUTHORIZED)

def rapport_vente_vendeur(request):
    vendeurs = Vendeur.objects.all()
    for v in vendeurs:
        ventes = Sale.objects.filter(seller=v)
        v.nb_ventes = ventes.count()
        v.total_ventes = ventes.aggregate(total=Sum('price'))['total'] or 0
    return render(request, 'rapport_vente_vendeur.html', {'vendeurs': vendeurs})


def accueil_vendeur(request):
    vendeur_id = request.session.get('vendeur_id')
    if not vendeur_id:
        return redirect('identification_vendeur')
    vendeur = Vendeur.objects.get(id=vendeur_id)
    return render(request, 'accueil_vendeur.html', {'vendeur': vendeur})


def historique_vendeur(request, vendeur_id):
    vendeur = get_object_or_404(Vendeur, id=vendeur_id)
    date = request.GET.get('date')
    ventes = Sale.objects.filter(seller=vendeur)
    if date:
        ventes = ventes.filter(created_at__date=date)
    return render(request, 'historique_vendeur.html', {'vendeur': vendeur, 'ventes': ventes, 'date': date})

def logout_vendeur(request):
    try:
        del request.session['vendeur_id']
    except KeyError:
        pass
    logout(request)
    return redirect('identification_vendeur')

def base_context(request):
    return {'vendeur_id': request.session.get('vendeur_id')}

def historique_vente(request):
    vendeur_id = request.session.get('vendeur_id')
    if not vendeur_id:
        return redirect('identification_vendeur')
    vendeur = Vendeur.objects.get(id=vendeur_id)
    today = timezone.now().date()
    ventes = Sale.objects.filter(seller=vendeur, created_at__date=today)
    return render(request, 'historique_vente.html', {'vendeur': vendeur, 'ventes': ventes})

def rapport_vente_vendeur_print(request, vendeur_id=None):
    if vendeur_id:
        vendeur = Vendeur.objects.get(id=vendeur_id)
        ventes = Sale.objects.filter(seller=vendeur).order_by('-created_at')
    else:
        vendeur = None
        ventes = Sale.objects.all().order_by('-created_at')
    total_ventes = ventes.aggregate(total=Sum('price'))['total'] or 0
    return render(request, 'rapport_vente_vendeur_print.html', {'ventes': ventes, 'vendeur': vendeur, 'total_ventes': total_ventes})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'form': {}, 'errors': True})
    return render(request, 'login.html', {'form': {}})
