from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from django.shortcuts import render, redirect

def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = 'sales_management.urls.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.sales.urls')),
    path('', lambda request: redirect('login'), name='root_login'),
]