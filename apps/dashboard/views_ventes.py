from django.shortcuts import render

def ventes_list_view(request):
    ventes = Vente.objects.select_related('produit', 'vendeur').all()
    context = {
        'ventes': ventes,
    }
    return render(request, 'ventes_list.html', context)
