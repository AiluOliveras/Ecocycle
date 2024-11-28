from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class Procesos(models.Model):
    """
    Modelo APP. Se corresponde con un proceso inciado en bonita.
    """

    inicio = models.DateTimeField(default=timezone.now)
    fin = models.DateTimeField(blank=True, null=True)

    iniciado_por=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    id_bonita = models.IntegerField(blank=False)

    formulario = models.ForeignKey('Formularios', on_delete=models.CASCADE)

    CARGADO = 'cargado'
    ENTREGADO = 'entregado'
    RECIBIDO = 'recibido'
    CERRADO = 'cerrado'
    NOTIFICADO = 'notificado'
    PAGADO = 'pagado'

    ESTADO_CHOICES = [
        (CARGADO, 'Cargado'),
        (ENTREGADO, 'Entregado'),
        (RECIBIDO, 'Recibido'),
        (CERRADO, 'Cerrado'),
        (NOTIFICADO, 'Notificado'),
        (PAGADO, 'Pagado')
    ]

    estado = models.CharField(
        max_length=10, 
        choices=ESTADO_CHOICES, 
        default=CARGADO
    )

class Proceso_solicitante(models.Model):
    id_bonita = models.IntegerField(blank=False)
    username = models.CharField(max_length=100)