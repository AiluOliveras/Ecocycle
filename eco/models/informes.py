from django.db import models
from django.utils import timezone
import datetime

class Informes(models.Model):
    """
    Modelo APP. Se corresponde con los informes sobre el rendimiento en cada formulario.
    """

    fecha= models.DateTimeField(default=timezone.now, blank=True)

    cant_materiales_fallidos=models.IntegerField()
    kg_faltantes_total=models.DecimalField(max_digits=20, decimal_places=2)
    cant_materiales_exitosos=models.IntegerField()
    cant_mats_no_recibidos=models.IntegerField()

    monto_pagado=models.DecimalField(max_digits=20, decimal_places=2, null=False, default=0)
    pagado= models.BooleanField(default=False, blank=True)


    evaluacion= models.ForeignKey('Evaluacion', on_delete=models.SET_NULL,null=True) #id de su evaluacion, si tiene
