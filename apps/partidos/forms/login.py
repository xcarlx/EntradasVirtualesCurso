from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView


class FormLogin(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
