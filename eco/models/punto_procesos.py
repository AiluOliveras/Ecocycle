from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class Punto_proceso(models.Model):
    """
    Modelo APP. Se corresponde con un proceso inciado en bonita.
    """

    inicio = models.DateTimeField(default=timezone.now)

    iniciado_por=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    id_bonita = models.IntegerField(blank=False)

    punto = models.ForeignKey('Punto_recoleccion', on_delete=models.CASCADE)