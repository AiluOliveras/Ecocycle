from django.db import models

class Materiales(models.Model):
    """
    Se corresponde con los materiales traídos al punto de recolección de residuos.
    """

    cantidad=models.DecimalField(max_digits=20, decimal_places=2, null=False)
    tipo= models.ForeignKey('Tiposmateriales', on_delete=models.CASCADE)