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
from django.urls import path, include

app_name = 'partidos'

urlpatterns = [
    path('', include('apps.partidos.urls_total.login')),
    path('inicio/', include('apps.partidos.urls_total.inicio')),
    path('control_tickets/', include('apps.partidos.urls_total.control_tickets')),
    path('partido/', include('apps.partidos.urls_total.partido')),
    path('partido/tribunas/', include('apps.partidos.urls_total.tribunas')),
    path('partido/cupones/', include('apps.partidos.urls_total.cupones')),
    path('partido/tickets/', include('apps.partidos.urls_total.tickets')),
    path('control_cupones/', include('apps.partidos.urls_total.control_cupones')),

]
