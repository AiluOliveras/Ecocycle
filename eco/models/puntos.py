from django.db import models
from django.utils import timezone
import datetime

class Puntos(models.Model):
    """
    Modelo API. Corresponde a un centro de recolección.
    """

    nombre = models.CharField(max_length=100)
    materiales_posibles = models.ManyToManyField('Tiposmateriales') 