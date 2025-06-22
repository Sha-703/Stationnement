from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

handler404 = 'sales_management.urls.custom_404'
handler500 = 'sales_management.urls.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.sales.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('', __import__('apps.sales.views').sales.views.root_redirect, name='root_redirect'),
]