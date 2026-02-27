import io
import zipfile

import pandas as pd
import qrcode
from asgiref.sync import sync_to_async
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from apps.partidos.models import Tickets, Partidos


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "partidos/inicio/vista.html"
