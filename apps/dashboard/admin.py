from django.contrib import admin
from .models import Dashboard  # Remplacez DashboardModel par Dashboard

# Enregistrez le modèle Dashboard dans l'interface d'administration
@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('total_sales', 'total_transactions', 'last_sale_date')