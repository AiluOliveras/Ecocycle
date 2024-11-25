from django.db import models
from django.utils import timezone
import datetime

class Stock(models.Model):
    """
    Modelo APP. Corresponde a la cantidad de stock de cada material.
    """

    cantidad=models.DecimalField(max_digits=20, decimal_places=2, null=False, default=0)
    tipo_material = models.OneToOneField('Tiposmateriales',null=False,on_delete=models.CASCADE)