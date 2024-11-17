from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
#from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
#from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse
#from ..forms import UpdateUserForm
from django.contrib.auth.models import User
#from django.views.generic.edit import UpdateView
from django.views.generic import ListView
from ..models import Punto_recoleccion


class UsuariosList(ListView):
    model = User
    paginate_by = 6

    ordering = ['username']

    def get_queryset(self):
        #se ejecuta al traer el listado de recicladores; Por ejemplo al querer agregar uno a un punto.

        filtro_punto= self.request.GET.get("filtro_punto") #param para saber si es para filtrar users
        username = self.request.GET.get('username')
        if filtro_punto:
    
            punto= self.request.GET.get("punto_id")
            punto = Punto_recoleccion.objects.get(id=punto)

            #retorno users que no fueron asignados
            recicladores=[]
            for reci in punto.recicladores.all():
                recicladores.append(reci.id) #guardo gestores

            #filtro los que son gestores
            queryset = User.objects.exclude(id__in=recicladores)

            if (username):
                queryset = queryset.filter(username__icontains=username)

            queryset = queryset.filter(is_staff=False)
        else:
            #retorno todos los user
            queryset = User.objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super(UsuariosList, self).get_context_data(**kwargs) # GET de la data default
        context['filtro_punto'] = self.request.GET.get('filtro_punto', 'None')
        punto= self.request.GET.get("punto_id")

        context['punto_obj'] = Punto_recoleccion.objects.get(id=punto) # Agrego punto seleccionado al contexto

        return context