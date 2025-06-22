from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = 'sales_management.urls.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.sales.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('', __import__('apps.sales.views').sales.views.login_view, name='login_root'),
]