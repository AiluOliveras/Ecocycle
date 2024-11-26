from django.db import models
from django.utils import timezone
import datetime

class Solicitantes(models.Model):
    """
    Modelo APP. Corresponde a un solicitante a recolector.
    """

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=253)