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
from django.contrib import admin
from django.urls import path
from ..vistas import inicio, login, control_tickets, partido

app_name = 'partido'

urlpatterns = [
    path('partido/', partido.PartidoHomeView.as_view(), name='home'),
    path('partido/lista/', partido.PartidoListView.as_view(), name='lista'),
    path('partido/crear/', partido.PartidoCrearView.as_view(), name='crear'),
    path('partido/editar/<int:pk>/', partido.PartidoEditarView.as_view(), name='editar'),
    path('partido/eliminar/<int:pk>/', partido.PartidoEliminarView.as_view(), name='eliminar'),
    path('partido/detall/<int:pk>/', partido.DetalleView.as_view(), name='detalle'),
    path('partido/success', partido.SuccessView.as_view(), name='success'),

]
