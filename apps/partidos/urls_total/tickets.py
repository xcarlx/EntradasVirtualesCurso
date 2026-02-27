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
from ..vistas import tickets

app_name = 'tickets'

urlpatterns = [
    path('lista/<int:pk>/', tickets.TicketsListView.as_view(), name='lista'),
    path('agregar/<int:pk>/', tickets.AgregarticketView.as_view(), name='agregar'),
    path('success/<int:pk>/', tickets.SuccessView.as_view(), name='success'),
    path('exportar-excel/<int:pk>/', tickets.ExportarQRExcelView.as_view(), name='exportar_excel'),
    path('tickets_qr_zip/descargar/<int:pk>/', tickets.QREntradaZipView.as_view(), name='descargar_tickets_zip'),

]
