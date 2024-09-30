from django.db import models
from django.utils import timezone
import datetime

class Formularios(models.Model):
    """
    Se corresponde con los formularios de recolección semanal de residuos.
    """

    fecha= models.DateTimeField(default=timezone.now, blank=True)
    abierto= models.BooleanField(default=True, blank=True)