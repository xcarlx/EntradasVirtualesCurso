import base64
import uuid

from django.core.exceptions import ValidationError
from django.db import models, transaction, IntegrityError


# Create your models here.
def logo_path(instance, filename):
    return f'logos/{filename}'


class Equipos(models.Model):
    nombre = models.CharField(max_length=200)
    logo = models.ImageField(upload_to=logo_path)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        ordering = ['nombre']


class Tribunas(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Tribuna'
        verbose_name_plural = 'Tribunas'
        ordering = ['nombre']


def portada_path(instance, filename):
    return f'portada/{filename}'


class Partidos(models.Model):
    codigo = models.CharField(max_length=9)
    equipo_local = models.ForeignKey(Equipos, on_delete=models.CASCADE, verbose_name="Equipo Local",
                                     related_name="equipo_local")
    equipo_visitante = models.ForeignKey(Equipos, on_delete=models.CASCADE, verbose_name="Equipo Visitante",
                                         related_name="equipo_visitante")
    fecha = models.DateField(verbose_name="Fecha de Inicio")
    horas = models.TimeField(verbose_name="Horas")
    lugar = models.CharField(max_length=150, verbose_name="Lugar")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    portada = models.ImageField(upload_to=portada_path, verbose_name="Porta")
    partidos_tribunas = models.ManyToManyField(Tribunas, through="PartidosTribuna",
                                               through_fields=('partido', 'tribuna'),
                                               related_name="partidos_tribunas",
                                               blank=True)

    def __str__(self):
        return self.codigo

    class Meta:
        verbose_name = 'Partido'
        verbose_name_plural = 'Partidos'
        ordering = ['codigo']


class PartidosTribuna(models.Model):
    partido = models.ForeignKey(Partidos, on_delete=models.CASCADE, verbose_name="Partido")
    tribuna = models.ForeignKey(Tribunas, on_delete=models.CASCADE, verbose_name="Tribuna")
    precio_general = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Precio General")
    precio_menor_edad = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Precio Menor Edad")
    cantidad = models.PositiveIntegerField(default=0, verbose_name="Cantidad")
    cantidad_cortesia = models.PositiveIntegerField(default=0, verbose_name="Cantidad Cortesia")

    def __str__(self):
        return self.partido.codigo

    class Meta:
        verbose_name = 'Partido Tribuna'
        verbose_name_plural = 'Partidos Tribunas'
        ordering = ['partido', 'tribuna']
        unique_together = ["partido", "tribuna"]


class Cupones(models.Model):
    codigo = models.CharField(max_length=9, verbose_name="Código")
    dni = models.CharField(max_length=8, blank=True, null=True, verbose_name="Dni")
    nombres = models.CharField(max_length=45, blank=True, null=True, verbose_name="Nombres")
    apellidos = models.CharField(max_length=45, blank=True, null=True, verbose_name="Apellidos")
    correo = models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico")
    celular = models.CharField(max_length=11, blank=True, null=True, verbose_name="Celular")
    fecha_uso = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Uso")
    tribuna = models.ForeignKey(PartidosTribuna, on_delete=models.CASCADE)

    def codigo_uuid(self):
        return base64.b64encode(self.codigo.encode()).decode()

    def __str__(self):
        return self.codigo

    class Meta:
        verbose_name = 'Cupon'
        verbose_name_plural = 'Cupones'
        ordering = ['id']
        indexes = [
            models.Index(fields=["codigo"], name="idxCupon_codigo"),
        ]


class Tickets(models.Model):
    codigo = models.CharField(max_length=9)
    correlativo = models.PositiveIntegerField()
    es_cortesia = models.BooleanField(default=False, verbose_name="Es cortesía")
    ingreso = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de ingreso")
    partido_tribuna = models.ForeignKey(PartidosTribuna, on_delete=models.CASCADE)
    cupon = models.OneToOneField(Cupones, blank=True, null=True, on_delete=models.CASCADE, related_name="ticket")

    def __str__(self):
        return self.codigo

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['id']
        indexes = [
            models.Index(fields=["codigo"], name="idx_codigo"),
        ]
