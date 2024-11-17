from django.db import models

class Tiposmateriales(models.Model):
    """
    Modelo APP y API. Se corresponde al tipo de un material cargado.
    """

    nombre = models.CharField(max_length=100)