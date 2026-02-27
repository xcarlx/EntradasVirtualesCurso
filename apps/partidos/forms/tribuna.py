from django import forms

from apps.partidos.models import PartidosTribuna


class TribunaForm(forms.ModelForm):
    class Meta:
        model = PartidosTribuna
        fields = ['partido', 'tribuna', 'precio_general', 'precio_menor_edad']
        widgets = {
            'precio_general': forms.NumberInput(
                attrs={'class': 'form-control', "min": "0", "max": "300"}),
            'precio_menor_edad': forms.NumberInput(
                attrs={'class': 'form-control', "min": "0", "max": "300"}),
            # 'cantidad': forms.NumberInput(
            #     attrs={'class': 'form-control', "min": "0", "max": "5000", "step": "1"}),
            # 'cantidad_cortesia': forms.NumberInput(
            #     attrs={'class': 'form-control', "min": "0", "max": "5000", "step": "1"}),
        }

    def __init__(self, *args, **kwargs):
        super(TribunaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['partido'].widget = forms.HiddenInput()
        # if self.instance.pk is not None:
        # self.fields['codigo'].widget.attrs.update({'readonly': 'readonly'})
