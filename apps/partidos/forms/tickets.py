import uuid

from django import forms
from django.db import transaction

from apps.partidos.models import PartidosTribuna, Tribunas, Tickets, Cupones


class TicketsForm(forms.Form):
    tribuna = forms.ModelChoiceField(Tribunas.objects.none())
    cantidad = forms.IntegerField()
    cantidad_cortesia = forms.IntegerField()


    def __init__(self, pk, *args, **kwargs):
        self.pk = pk
        super(TicketsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['tribuna'].queryset = Tribunas.objects.filter(
            id__in=PartidosTribuna.objects.filter(partido_id=self.pk).values_list("tribuna_id", flat=True))
        # if self.instance.pk is not None:
        # self.fields['codigo'].widget.attrs.update({'readonly': 'readonly'})

    def _generar_codigo_unico(self):
        """Genera un código único de 9 caracteres para un partido."""
        while True:
            codigo = uuid.uuid4().hex[:9].upper()
            if not Tickets.objects.filter(
                    partido_tribuna__partido_id=self.pk,
                    codigo=codigo
            ).exists():
                return codigo

    def correlativo(self):
        tickets = Tickets.objects.filter(partido_tribuna__partido_id=self.pk).all().order_by('id')
        if not tickets.exists():
            return 1
        else:
            return tickets.last().correlativo + 1

    @transaction.atomic
    def save(self):
        tribuna = self.cleaned_data['tribuna']
        cantidad = self.cleaned_data['cantidad']
        cantidad_cortesia = self.cleaned_data['cantidad_cortesia']
        partido = self.pk
        partido_tribuna = PartidosTribuna.objects.get(partido_id=partido, tribuna=tribuna)
        for _ in range(cantidad_cortesia):
            codigo = self._generar_codigo_unico()
            cupon = Cupones.objects.create(
                codigo=codigo,
                tribuna=partido_tribuna,
            )
            Tickets.objects.create(
                codigo=codigo,
                correlativo=self.correlativo(),
                es_cortesia=True,
                partido_tribuna=partido_tribuna,
                cupon=cupon,
            )

        # Crear tickets normales
        for _ in range(cantidad):
            codigo = self._generar_codigo_unico()
            Tickets.objects.create(
                codigo=codigo,
                correlativo=self.correlativo(),
                es_cortesia=False,
                partido_tribuna=partido_tribuna,
            )

        partido_tribuna.cantidad_cortesia = Tickets.objects.filter(partido_tribuna=partido_tribuna,
                                                                   es_cortesia=True).count()
        partido_tribuna.cantidad = Tickets.objects.filter(partido_tribuna=partido_tribuna, es_cortesia=False).count()
        partido_tribuna.save()
