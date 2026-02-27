import asyncio
import io
import zipfile

import qrcode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, TemplateView

from apps.partidos.forms.tickets import TicketsForm
from apps.partidos.models import Tickets, Partidos, PartidosTribuna
import pandas as pd


class TicketsListView(LoginRequiredMixin, ListView):
    model = Tickets
    template_name = "partidos/tickets/lista.html"
    paginate_by = 10
    ordering = '-id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['pk'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        return super().get_queryset().filter(partido_tribuna__partido_id=self.kwargs['pk'])


class AgregarticketView(LoginRequiredMixin, FormView):
    template_name = "partidos/tickets/form.html"
    form_class = TicketsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'pk': self.kwargs['pk']})
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('partidos:tickets:success', kwargs={'pk': self.kwargs['pk']})


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = "partidos/tickets/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['pk'] = self.kwargs['pk']
        return context


class ExportarQRExcelView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Consultas síncronas normales
        tickets = Tickets.objects.filter(
            partido_tribuna__partido__id=self.kwargs['pk']
        ).values(
            "codigo", "correlativo", "es_cortesia", "partido_tribuna__tribuna__nombre"
        ).order_by("correlativo")

        # Datos para el DataFrame
        datos = {
            "CODIGO": [t["codigo"] for t in tickets],
            "CORRELATIVO": [t["correlativo"] for t in tickets],
            "ES CORTESIA": [t["es_cortesia"] for t in tickets],
            "TRIBUNA": [t["partido_tribuna__tribuna__nombre"] for t in tickets],
        }

        df = pd.DataFrame(datos)

        # Crear respuesta HTTP con tipo Excel
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="reporte.xlsx"'

        # Exportar DataFrame a Excel
        with pd.ExcelWriter(response, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Reporte")

        return response


# --- Función para generar QR ---
def generar_qr_png(data: str) -> bytes:
    """
    Genera un código QR en formato PNG y devuelve los bytes.
    Se ejecuta en un hilo para no bloquear el loop de eventos.
    """

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img_qr.save(buffer, format="PNG")
    return buffer.getvalue()


# --- Función para generar ZIP ---
def generate_zip(files):
    """
    Genera un archivo ZIP en memoria con los archivos proporcionados.
    Cada elemento de `files` debe ser una tupla (nombre, contenido_bytes).
    """

    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for nombre, contenido in files:
            zf.writestr(nombre, contenido)
    return mem_zip.getvalue()


# --- Vista principal ---
class QREntradaZipView(View):

    def get(self, request, *args, **kwargs):
        # ORM (síncrono) → sync_to_async
        partido = Partidos.objects.get(pk=self.kwargs['pk'])

        tickets_normales = Tickets.objects.filter(partido_tribuna__partido=partido, es_cortesia=False)

        # Generar QR en paralelo
        def generar_para_ticket(ticket):
            reporte = generar_qr_png(ticket.codigo)
            nombre = f"{ticket.partido_tribuna.tribuna.nombre}/{ticket.correlativo}-{ticket.codigo}.png"
            return (nombre, reporte)

        lista_pdf = (generar_para_ticket(ticket) for ticket in tickets_normales)

        # Generar ZIP
        zipticket = generate_zip(lista_pdf)

        # Respuesta HTTP
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=tickets_qr.zip'
        response.write(zipticket)
        return response
