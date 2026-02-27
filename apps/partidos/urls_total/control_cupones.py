from django.urls import path

from apps.partidos.vistas import control_cupones

app_name = "control_cupones"
urlpatterns = [
    path('', control_cupones.ValidarCuponView.as_view(), name='vista'),
    path('canjear_cupon/<int:pk>/', control_cupones.CanjearCuponView.as_view(), name='canjear-cupon'),
    path('success/<str:codigo>/', control_cupones.SuccessView.as_view(), name='success'),
]
