from django.contrib import admin

from .models import Equipos, Tribunas, Tickets, Partidos, PartidosTribuna

@admin.register(Equipos)
class EquiposAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'logo']

@admin.register(Tribunas)
class TribunasAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(Tickets)
class TicketsAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'correlativo', 'es_cortesia', 'ingreso']

@admin.register(Partidos)
class PartidosAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'equipo_local', 'equipo_visitante', 'fecha', 'horas', 'lugar', 'activo']

@admin.register(PartidosTribuna)
class PartidosTribunaAdmin(admin.ModelAdmin):
    list_display = ['precio_general', 'precio_menor_edad', 'cantidad', 'cantidad_cortesia']
