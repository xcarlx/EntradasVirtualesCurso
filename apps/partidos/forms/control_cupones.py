from django import forms

from apps.partidos.models import Cupones, Partidos


class ValidarCuponForm(forms.Form):
    codigo = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control fs-4', 'placeholder': 'Codigo', 'required': 'true',
                   'autofocus': 'autofocus', 'autocomplete': 'off', 'minlength': "9", 'maxlength': "9"}), )

    def save(self):
        cupon = self.cleaned_data['codigo']
        partido = Partidos.objects.filter(activo=True).order_by("id").last()
        cupones = Cupones.objects.filter(codigo=cupon, tribuna__partido=partido, fecha_uso=None)
        if cupones.exists():
            return cupones.last()
        return None


class RegistroCuponForm(forms.ModelForm):
    class Meta:
        model = Cupones
        fields = ['dni', 'nombres', 'apellidos', 'correo', 'celular']
        widgets = {}

    def __init__(self, *args, **kwargs):
        super(RegistroCuponForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['autocomplete'] = 'off'
            self.fields[field].required = True
