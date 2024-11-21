from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class Procesos(models.Model):
    """
    Modelo APP. Se corresponde con un proceso inciado en bonita.
    """

    inicio = models.DateTimeField(default=timezone.now)
    fin = models.DateTimeField(blank=True, null=True)

    iniciado_por=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    id_bonita = models.IntegerField(blank=False)

    formulario = models.ForeignKey('Formularios', on_delete=models.CASCADE)