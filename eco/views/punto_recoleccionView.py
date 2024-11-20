from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from ..models import Punto_recoleccion
from django.contrib.auth.models import User

from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from ..forms import Punto_recoleccionForm
from django.http import HttpResponseRedirect, HttpResponse

from eco.bonita.access import Access
from eco.bonita.process import Process

class Punto_recoleccionCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = Punto_recoleccionForm
    success_message = 'Punto de recolección creado exitosamente!'
    permission_required = 'add_punto_recoleccion'
    
    def get_success_url(self):
        return reverse('inicio')

class Punto_recoleccionList(ListView):
    model = Punto_recoleccion
    paginate_by = 15

    ordering = ['-id']

    def get_queryset(self):
        nombre = self.request.GET.get('nombre')
        if nombre:
            return Punto_recoleccion.objects.filter(nombre__icontains=nombre)
        else:
            return Punto_recoleccion.objects.all()

def create_reciclador_punto(request, *args, **kwargs):
    """ Asigna un punto de recolección a un reciclador.

    Args:
        punto: FK con tabla punto recolección, es el punto que se quiere asignar al recolector
        reciclador: FK con tabla usuarios, es el recolector al que se le asigna el punto

    Returns:
        Redirección hacia el template de puntos de recolección con un mensaje de operacion exitosa.
    
    Raises:
        HttpResponse con mensaje de error en caso de ocurrir algun problema de indices.

    """

    if request.user.is_staff:
        from django.contrib.auth.models import User
        reciclador= request.GET.get("reciclador")
        punto= request.GET.get("punto")

        if reciclador and punto:
            #checkear que no exista ya la unión

            #se asigna el punto
            punto_up = Punto_recoleccion.objects.get(id=punto)
            reciclador_up = User.objects.get(id=reciclador)
            punto_up.recicladores.add(reciclador_up)

            messages.success(request,('Reciclador añadido exitosamente!'))
            
            return HttpResponseRedirect('/punto_recoleccion/listar/recicladores/?punto='+punto)
    
    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")

def destroy_reciclador_punto(request, *args, **kwargs):
    """ Da de baja a un reciclador de un punto.

    Args:
        punto: FK con tabla punto recoleccion, es el punto sobre el cual se da de baja
        reciclador: FK con tabla usuarios, es el usuario que quiere darse de baja del punto

    Returns:
        Redirección hacia el template de recicladores con un mensaje de operacion exitosa.
    
    Raises:
        HttpResponse con mensaje de error en caso de ocurrir algun problema de indices.

    """

    if request.user.is_staff:
        from django.contrib.auth.models import User
        reciclador= request.GET.get("reciclador")
        punto= request.GET.get("punto")

        if punto and reciclador:

            #se elimina permiso del reciclador sobre el punto dado
            punto_up = Punto_recoleccion.objects.get(id=punto)
            reciclador_up = User.objects.get(id=reciclador)
            punto_up.recicladores.remove(reciclador_up)

            messages.success(request,('Punto removido del reciclador exitosamente!'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #recargo pag  base

    return HttpResponse("Hubo un error, por favor regrese a la página anterior.")

class Punto_recoleccion_recicladorList(ListView):
    model = Punto_recoleccion
    paginate_by = 30

    ordering = ['nombre']

    def get_queryset(self):
        reciclador= self.request.user.id
        return Punto_recoleccion.objects.filter(recicladores__id=reciclador)