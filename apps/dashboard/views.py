from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum, Count, Q, F
from django.utils.timezone import now
from django.db import models
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from apps.sales.models import Sale, Produit, Vendeur, POS  # Ajout de POS à l'import
from .models import Dashboard
from rest_framework.decorators import api_view
from .serializers import DashboardSerializer
from calendar import month_name
import csv
import datetime
from django.views.generic import TemplateView
import json
from itertools import chain

@api_view(['GET'])
def dashboard_overview(request):
    data = DashboardData.objects.all()
    serializer = DashboardSerializer(data, many=True)
    return JsonResponse(serializer.data, safe=False)

def dashboard_statistics(request):
    filter_type = request.GET.get('filter', 'monthly')

    if filter_type == 'daily':
        sales = Sale.objects.annotate(period=TruncDay('created_at')).values('period').annotate(
            total=Sum('price'),
            product_name=F('produit__nom_produit'),
            seller_name=F('seller__nom_du_vendeur')
        )
    elif filter_type == 'monthly':
        sales = Sale.objects.annotate(period=TruncMonth('created_at')).values('period').annotate(
            total=Sum('price'),
            product_name=F('produit__nom_produit'),
            seller_name=F('seller__nom_du_vendeur')
        )
    elif filter_type == 'yearly':
        sales = Sale.objects.annotate(period=TruncYear('created_at')).values('period').annotate(
            total=Sum('price'),
            product_name=F('produit__nom_produit'),
            seller_name=F('seller__nom_du_vendeur')
        )
    else:
        sales = []

    sales_data = [
        {
            'period': sale['period'].strftime('%Y-%m-%d') if isinstance(sale['period'], datetime.date) else str(sale['period']),
            'total': sale['total'],
            'product_name': sale['product_name'],
            'seller_name': sale['seller_name']
        }
        for sale in sales
    ]

    return JsonResponse({
        'sales_by_day': sales_data if filter_type == 'daily' else [],
        'sales_by_month': sales_data if filter_type == 'monthly' else [],
        'sales_by_year': sales_data if filter_type == 'yearly' else [],
    })

def sales_statistics(request):
    # Calculer les statistiques des ventes
    total_sales = Sale.objects.aggregate(total_sales=Sum('total_price'))['total_sales'] or 0
    total_transactions = Sale.objects.count()
    return JsonResponse({
        'total_sales': total_sales,
        'total_transactions': total_transactions
    })

def dashboard_view(request):
    # Récupérer le filtre
    filter_type = request.GET.get('filter', 'monthly')
    sales = Sale.objects.select_related('produit', 'seller').all()
    ventes = Sale.objects.select_related('produit', 'seller').all()  # Remplace Vente par Sale

    # Fusionner les ventes des deux apps
    all_sales = sales.union(ventes)

    # Pour le graphique, on ne prend que les ventes de Sale (pour compatibilité existante)
    # Mais pour les totaux, on additionne tout
    total_sales = sum([getattr(s, 'price', getattr(s, 'prix_total', 0)) for s in all_sales])
    total_products = Produit.objects.count()
    total_sellers = Vendeur.objects.count()
    total_transactions = len(all_sales)
    total_pos = POS.objects.count()

    # Filtrer les ventes pour le graphique selon le filtre sélectionné
    if filter_type == 'daily':
        sales_by_period = (
            sales.annotate(period=TruncDay('created_at'))
            .values('period')
            .annotate(total_sales=Sum('price'))
            .order_by('period')
        )
        labels = [sale['period'].strftime('%Y-%m-%d') for sale in sales_by_period]
    elif filter_type == 'yearly':
        sales_by_period = (
            sales.annotate(period=TruncYear('created_at'))
            .values('period')
            .annotate(total_sales=Sum('price'))
            .order_by('period')
        )
        labels = [str(sale['period'].year) for sale in sales_by_period]
    else:  # monthly par défaut
        sales_by_period = (
            sales.annotate(period=TruncMonth('created_at'))
            .values('period')
            .annotate(total_sales=Sum('price'))
            .order_by('period')
        )
        labels = [sale['period'].strftime('%Y-%m') for sale in sales_by_period]

    sales_chart_data = {
        'labels': json.dumps(labels),
        'data': json.dumps([float(sale['total_sales']) for sale in sales_by_period]),
    }

    # Statistiques globales
    total_sales = sales.aggregate(total_sales=Sum('price'))['total_sales'] or 0
    total_products = Produit.objects.count()
    total_sellers = Vendeur.objects.count()
    total_transactions = sales.count()
    total_pos = POS.objects.count()

    # Répartition des ventes par vendeur (toujours sur toutes les ventes)
    sales_by_seller = (
        sales.values('seller__nom_du_vendeur')
        .annotate(total_sales=Sum('price'))
        .order_by('-total_sales')
    )
    pie_chart_data = {
        'labels': json.dumps([item['seller__nom_du_vendeur'] for item in sales_by_seller]),
        'data': json.dumps([float(item['total_sales']) for item in sales_by_seller]),
    }

    # 5 dernières ventes
    last_sales = Sale.objects.select_related('produit', 'seller').order_by('-created_at')[:5]
    context = {
        'sales': all_sales,
        'total_sales': total_sales,
        'total_products': total_products,
        'total_sellers': total_sellers,
        'total_transactions': total_transactions,
        'total_pos': total_pos,
        'sales_chart_data': sales_chart_data,
        'pie_chart_data': pie_chart_data,
        'last_sales': last_sales,
    }
    return render(request, 'dashboard.html', context)

def sales_list_view(request):
    sales = Sale.objects.select_related('produit', 'seller').all()  # Inclure les relations avec Produit et Vendeur
    context = {
        'sales': sales,
    }
    return render(request, 'sales_list.html', context)

def export_sales_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales.csv"'

    writer = csv.writer(response)
    writer.writerow(['Produit', 'Vendeur', 'Prix', 'Date'])

    for sale in Sale.objects.all():
        writer.writerow([sale.produit.nom_produit, sale.seller.nom_du_vendeur, sale.price, sale.created_at])

    return response

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_pos'] = POS.objects.count()
        context['pos_list'] = POS.objects.all()
        return context