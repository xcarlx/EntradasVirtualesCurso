import base64
import io

import qrcode
from asgiref.sync import sync_to_async
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView
from numpy.f2py.crackfortran import quiet
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from apps.partidos.models import Cupones, Partidos, Tickets
import pandas as pd


class CuponesListView(LoginRequiredMixin, ListView):
    model = Cupones
    template_name = "partidos/cupones/lista.html"
    paginate_by = 10
    ordering = '-id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['pk'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        return super().get_queryset().filter(tribuna__partido_id=self.kwargs['pk'])


class ExportarCuponesExcelView(View):
    async def get(self, request, *args, **kwargs):
        # Consultas síncronas envueltas en async
        partido = await sync_to_async(lambda: Partidos.objects.get(pk=self.kwargs['pk']))()
        tickets = await sync_to_async(
            lambda: list(
                Cupones.objects.filter(tribuna__partido=partido)
                .values("codigo", "tribuna__tribuna__nombre").order_by(
                    "id")
            )
        )()
        # Datos para el DataFrame
        datos = {
            "CODIGO": [],
            "TRIBUNA": [],
        }

        for t in tickets:
            datos["CODIGO"].append(t["codigo"])
            datos["TRIBUNA"].append(t["tribuna__tribuna__nombre"])

        df = pd.DataFrame(datos)
        # Crear respuesta HTTP con tipo Excel
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="reporte.xlsx"'
        # Exportar DataFrame a Excel
        # (esto sigue siendo síncrono, pero está bien porque es rápido en memoria)
        with pd.ExcelWriter(response, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Reporte")

        return response


class GenerarCortesiaPDFView(View):
    def get(self, request, *args, **kwargs):
        # Obtener el ticket
        ticket = Tickets.objects.get(codigo=str(base64.b64decode(self.kwargs['codigo']).decode()))

        # Usar la función auxiliar para generar el PDF
        pdf_bytes = generar_pdf_cortesia(ticket)

        # Devolver como respuesta HTTP
        response = HttpResponse(
            pdf_bytes,
            content_type="application/pdf"
        )
        response["Content-Disposition"] = f'filename="cortesia_{ticket.codigo}.pdf"'
        # response["Content-Disposition"] = f'attachment;filename="cortesia_{ticket.codigo}.pdf"'
        return response


def generar_pdf_cortesia(ticket):
    # Data para el QR
    data_qr = ticket.codigo

    # Generar QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(data_qr)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white")

    qr_buffer = io.BytesIO()
    img_qr.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    qr_image = ImageReader(qr_buffer)

    # Crear PDF
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=(14 * cm, 5 * cm))
    width, height = (14 * cm, 5 * cm)

    # Fondo institucional
    fondo_path = ticket.partido_tribuna.partido.portada.path
    fondo_image = ImageReader(fondo_path)
    c.drawImage(fondo_image, 0, 0, width=width, height=height)

    # Insertar QR
    c.drawImage(qr_image, 260, 25, width=1.7 * cm, height=1.7 * cm)
    # c.drawImage(qr_image, 335, 40, width=1.7 * cm, height=1.7 * cm)
    c.drawImage(qr_image, 10, 36, width=1.7 * cm, height=1.7 * cm)

    # Texto institucional
    c.setFont("Helvetica-Bold", 8)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(265, 78, "Cortesia")
    c.drawString(265, 90, f"{ticket.partido_tribuna.tribuna.nombre}")
    c.setFont("Helvetica", 6)
    c.drawString(125, 32, f"{ticket.cupon.nombres} {ticket.cupon.apellidos} ")
    c.drawString(103, 21, f"{ticket.cupon.dni} ")
    c.drawString(265, 7, f"{str(ticket.correlativo).zfill(9)}")
    c.drawString(345, 7, f"{str(ticket.correlativo).zfill(9)}")
    c.drawString(14, 7, f"{str(ticket.correlativo).zfill(9)}")

    barcode = code128.Code128(ticket.correlativo, barHeight=1.5 * cm, barWidth=1.2)

    c.translate(380, 10)
    c.rotate(90)
    barcode.drawOn(c, 15, 0)
    c.saveState()
    c.restoreState()

    c.showPage()
    c.save()

    pdf_buffer.seek(0)
    # ✅ devolver bytes, no BytesIO
    return pdf_buffer.getvalue()
