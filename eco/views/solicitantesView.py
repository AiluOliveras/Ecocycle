from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Solicitantes
from django.contrib.auth.models import User

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from ..forms import SolicitantesForm
from django.http import HttpResponseRedirect, HttpResponse

from eco.bonita.access import Access
from eco.bonita.process import Process


class SolicitantesCreate(SuccessMessageMixin, CreateView):
    form_class = SolicitantesForm
    success_message = 'Solicitud de registro creada exitosamente!'
    
    def get_success_url(self):
        return reverse('inicio')

class SolicitantesList(ListView):
    model = Solicitantes
    paginate_by = 15

    ordering = ['-id']

    def get_queryset(self):
        return Solicitantes.objects.all()

class SolicitantesDelete(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Solicitantes
    form = SolicitantesForm
    fields = "__all__"
    permission_required = 'delete_solicitantes'

    def get_success_url(self):
        success_message = 'Solicitud rechazada.'
        messages.success (self.request, (success_message))
        return reverse('solicitantes')


def create_reciclador(request,pk):
    """ Da de alta un reciclador en la bbdd como usuario al aceptarse la solicitud.

    """

    if request.user.is_staff:
        from django.contrib.auth.models import User

        if pk:

            #busco el solicitante
            solicitante = Solicitantes.objects.get(id=pk)

            #verifica si existe el user
            try:
                user=User.objects.get(username=solicitante.username)
                #el user existe, genero otro username
                ult_id=(User.objects.latest('id')).id
                ult_id=ult_id+1
                solicitante_usuario=(str(solicitante.username)+str(ult_id))
                User.objects.create_user(username=solicitante_usuario,email=solicitante.email,password='123',first_name=solicitante.nombre,last_name=solicitante.apellido,is_superuser=True,is_staff=False)

            except User.DoesNotExist:
                #el username está disponible, crea usuario
                User.objects.create_user(username=solicitante.username,email=solicitante.email,password='123',first_name=solicitante.nombre,last_name=solicitante.apellido,is_superuser=True,is_staff=False)

            #borro la solicitud
            Solicitantes.objects.filter(id=pk).delete()

            messages.success(request,('Solicitante creado exitosamente!'))
            
            return HttpResponseRedirect('/solicitudes')
    
    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")