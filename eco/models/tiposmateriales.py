from django.db import models

class Tiposmateriales(models.Model):
    """
    Modelo APP y API. Se corresponde al tipo de un material cargado.
    """

    nombre = models.CharField(max_length=100)

    #campo para la APP unicamente
    precio_por_kg = models.DecimalField(max_digits=20, decimal_places=2, null=False, default=20)

    trabajado = models.BooleanField(default=False)