import base64
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, ListView

from apps.partidos.models import Tickets, Partidos


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "partidos/control_tickets/vista.html"


class ValidarTicketView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        codigo = self.request.POST.get('codigo')
        partido = Partidos.objects.filter(activo=True).last()
        tikect = get_object_or_404(Tickets, codigo=codigo,
                                   partido_tribuna__partido=partido)
        if tikect.ingreso is None:
            tikect.ingreso = timezone.now()
            tikect.save()
            return JsonResponse({
                'status': True,
                'pk': tikect.pk
            })
        else:
            return JsonResponse({
                'status': False,
                'pk': tikect.pk,
                "mensaje": "Ticket Utilizado"
            })


class ListarTicketsView(LoginRequiredMixin, ListView):
    model = Tickets
    template_name = 'partidos/control_tickets/lista.html'
    paginate_by = 10
    ordering = '-ingreso'

    def get_queryset(self):
        partido = Partidos.objects.filter(activo=True).last()
        return super().get_queryset().filter(ingreso__isnull=False, partido_tribuna__partido=partido)
