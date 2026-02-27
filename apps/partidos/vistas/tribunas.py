from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView

from apps.partidos.forms.tribuna import TribunaForm
from apps.partidos.models import PartidosTribuna


class TribunasListView(LoginRequiredMixin, ListView):
    model = PartidosTribuna
    template_name = "partidos/tribunas/lista.html"
    paginate_by = 10
    ordering = '-id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['pk'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        return super().get_queryset().filter(partido_id=self.kwargs['pk'])


class TribunaCrearView(LoginRequiredMixin, CreateView):
    model = PartidosTribuna
    form_class = TribunaForm
    template_name = "partidos/tribunas/form.html"

    def get_success_url(self):
        return reverse_lazy('partidos:tribunas:success', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['pk'] = self.kwargs['pk']
        return context

    def get_initial(self):
        initial = {
            "partido": self.kwargs['pk'],
        }
        return initial

    # def form_valid(self, form):
    #     partido_id = self.kwargs['pk']
    #     partido_tribuna = form.save(commit=False)
    #     partido_tribuna.partido_id = partido_id
    #     partido_tribuna.save()
    #     return super().form_valid(partido_tribuna)


class TribunaEditarView(LoginRequiredMixin, UpdateView):
    model = PartidosTribuna
    form_class = TribunaForm
    template_name = "partidos/tribunas/form.html"
    success_url = reverse_lazy('partidos:tribunas:success')

    def get_success_url(self):
        return reverse_lazy('partidos:tribunas:success', kwargs={'pk': self.get_object().partido_id})


class TribunaEliminarView(LoginRequiredMixin, DeleteView):
    model = PartidosTribuna
    template_name = "partidos/tribunas/eliminar.html"
    success_url = reverse_lazy('partidos:tribunas:success')

    def get_success_url(self):
        return reverse_lazy('partidos:tribunas:success', kwargs={'pk': self.get_object().partido_id})


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = "partidos/tribunas/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['pk'] = self.kwargs['pk']
        return context
