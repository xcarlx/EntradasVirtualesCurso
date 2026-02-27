import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from pycparser.c_ast import Return

from apps.partidos.forms.partido import PartidoForm
from apps.partidos.models import Partidos


class PartidoHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'partidos/partido/vista.html'


class PartidoListView(LoginRequiredMixin, ListView):
    template_name = 'partidos/partido/lista.html'
    model = Partidos
    ordering = '-pk'
    paginate_by = 10
    # search_fields = ['titulo', 'descricao']


class PartidoCrearView(LoginRequiredMixin, CreateView):
    model = Partidos
    form_class = PartidoForm
    template_name = "partidos/partido/form.html"
    success_url = reverse_lazy('partidos:partido:success')

    def get_initial(self):
        initial = super().get_initial()
        initial['codigo'] = uuid.uuid4().hex[:9].upper()
        return initial

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class PartidoEditarView(LoginRequiredMixin, UpdateView):
    model = Partidos
    form_class = PartidoForm
    template_name = "partidos/partido/form.html"
    success_url = reverse_lazy('partidos:partido:success')

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class PartidoEliminarView(LoginRequiredMixin, DeleteView):
    model = Partidos
    template_name = "partidos/partido/eliminar.html"
    success_url = reverse_lazy('partidos:partido:success')


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = "partidos/partido/success.html"


class DetalleView(LoginRequiredMixin, DetailView):
    model = Partidos
    template_name = "partidos/partido/detalle.html"
