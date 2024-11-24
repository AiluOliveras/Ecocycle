from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class Punto_recoleccion(models.Model):
    """
    Modelo APP. Corresponde a un punto de recolección registrado por un centro de recolección.
    Este será asignado a diversos recicladores.
    """

    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    verificado = models.BooleanField(default=False) # El empleado los verifica

    recicladores = models.ManyToManyField(User)