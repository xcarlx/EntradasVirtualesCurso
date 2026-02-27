from django import forms

from apps.partidos.models import Partidos


class PartidoForm(forms.ModelForm):
    class Meta:
        model = Partidos
        fields = ['codigo', 'equipo_local', 'equipo_visitante', 'fecha', 'horas', 'lugar', 'activo', 'portada']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', "type": "date"}, format='%Y-%m-%d'),
            'horas': forms.TimeInput(attrs={'class': 'form-control', "type": "time"}, format='%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(PartidoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'activo':
                self.fields[field].widget.attrs.update({'class': 'form-control'})

        if self.instance.pk is not None:
            self.fields['codigo'].widget.attrs.update({'readonly': 'readonly'})
