import base64

from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, FormView, UpdateView

from apps.partidos.forms.control_cupones import ValidarCuponForm, RegistroCuponForm
from apps.partidos.models import Cupones, Partidos


class ValidarCuponView(FormView):
    template_name = "partidos/control_cupones/vista.html"
    form_class = ValidarCuponForm
    cupon = None

    def form_valid(self, form):
        self.cupon = form.save()
        return super(ValidarCuponView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('partidos:control_cupones:success',
                            kwargs={'codigo': self.cupon.codigo_uuid() if self.cupon else '0'})


class CanjearCuponView(UpdateView):
    template_name = "partidos/control_cupones/canjear_cupon.html"
    model = Cupones
    form_class = RegistroCuponForm

    def form_valid(self, form):
        cupon = form.save(commit=False)
        cupon.fecha_uso = timezone.now()
        cupon.save()
        return super(CanjearCuponView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('partidos:control_cupones:success',
                            kwargs={'codigo': self.get_object().codigo_uuid()})


class SuccessView(TemplateView):
    template_name = "partidos/control_cupones/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.kwargs['codigo'] != "0":
            cupones = Cupones.objects.filter(
                codigo=f"{base64.b64decode(self.kwargs['codigo']).decode()}",
                tribuna__partido=Partidos.objects.filter(activo=True).last())
            context['existe'] = cupones.exists()
            context['cupon'] = cupones.last()
        return context
