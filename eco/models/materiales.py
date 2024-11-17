from django.db import models
from django.urls import reverse

class Materiales(models.Model):
    """
    Modelo APP. Se corresponde con los materiales traídos al punto de recolección de residuos.
    """

    cantidad=models.DecimalField(max_digits=20, decimal_places=2, null=False)
    tipo= models.ForeignKey('Tiposmateriales', on_delete=models.CASCADE)
    
    formulario= models.ForeignKey('Formularios', on_delete=models.CASCADE, null=True, default=None)

    def get_absolute_url(self):
        """
        Devuelve la URL para acceder a la vista detalle de este form.
        """
        if self.formulario:
            return reverse("formularios/detalle", kwargs={'pk': self.formulario.pk})
        else:
            # Handle case where formulario is not set
            return "#"
