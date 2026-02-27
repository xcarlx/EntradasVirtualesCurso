"""
URL configuration for EntradasVirtuales project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from ..vistas import cupones

app_name = 'cupones'

urlpatterns = [
    path('lista/<int:pk>/', cupones.CuponesListView.as_view(), name='lista'),
    path('ticket-pdf/<str:codigo>/', cupones.GenerarCortesiaPDFView.as_view(), name='ticket-pdf'),
    path('exportar/<int:pk>/', cupones.ExportarCuponesExcelView.as_view(), name='exportar_excel'),
]
