from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from apps.partidos.forms.login import FormLogin


class LoginView(FormView):
    template_name = "partidos/inicio/login.html"
    form_class = FormLogin
    success_url = reverse_lazy('partidos:inicio:home')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(redirect_to=reverse_lazy('partidos:inicio:home'))
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            return self.form_invalid(form)
        return super(LoginView, self).form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return HttpResponseRedirect(reverse_lazy('partidos:inicio:home'))
