from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class Formularios(models.Model):
    """
    Modelo APP. Se corresponde con los formularios de recolección semanal de residuos.
    """

    fecha= models.DateTimeField(default=timezone.now, blank=True)
    abierto= models.BooleanField(default=True, blank=True)

    reciclador=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)