from django.db import models
from django.utils import timezone
import datetime


class Solicitudes_red(models.Model):
    """
    Modelo APP. Corresponde a las solicitudes aceptadas de la red.
    """

    cantidad=models.DecimalField(max_digits=20, decimal_places=2, null=False, default=0)
    tipo_material= models.ForeignKey('Tiposmateriales', on_delete=models.CASCADE,null=True)
    estado = models.CharField(max_length=1) # P= pendiente, A= aprobado, R= rechazado