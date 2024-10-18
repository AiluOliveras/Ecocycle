from django.db import models
from django.utils import timezone
import datetime

class Ordenes(models.Model):
    """
    Modelo API. Corresponde a la orden creada por un depósito para los puntos de recolección.
    """

    cantidad=models.DecimalField(max_digits=20, decimal_places=2, null=False)
    tipo= models.ForeignKey('Tiposmateriales', on_delete=models.CASCADE)
    reservado= models.BooleanField(default=False)
    entregado= models.BooleanField(default=False)
    
    proveedor= models.ForeignKey('Puntos', on_delete=models.CASCADE,null=True) #id del punto en caso de que esté reservado