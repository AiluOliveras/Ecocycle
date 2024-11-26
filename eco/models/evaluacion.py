from django.db import models
from django.utils import timezone
import datetime

class Evaluacion(models.Model):
    """
    Modelo APP. Se realiza una evaluacion cada 2 semanas sobre el rendimiento de los recicladores.
    """

    fecha_inicio= models.DateTimeField(default=timezone.now, blank=True)
    fecha_fin= models.DateTimeField(default=timezone.now, blank=True)