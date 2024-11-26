"""ecocycle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from eco.views import MaterialesCreate, FormulariosDetail, FormulariosCreate, cerrar_formulario, bonita, OrdenesList, OrdenReservaUpdate, OrdenEntregaUpdate, PuntoMaterialRegistro,Punto_recoleccionCreate,Punto_recoleccionList,UsuariosList
from eco.views import RecicladoresList, destroy_reciclador_punto,create_reciclador_punto, Punto_recoleccion_recicladorList, Materiales_RecibidosCreate
from eco.views import verificar_punto, procesar_diferencias_formulario, marcar_informe_pagado, hacer_evaluacion, EvaluacionDetail
from django.contrib.auth.views import LoginView, LogoutView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('bienvenida/', include('eco.urls')),

    path('home/', LoginView.as_view()),
    path("bonita", bonita, name="bonita"),
    
    path('inicio/', FormulariosCreate.as_view(template_name = "formularios/create.html"),name='inicio'),
    path('evaluar/', hacer_evaluacion),
    path('evaluar/<int:pk>', EvaluacionDetail.as_view(template_name = "evaluacion/detail.html"),name='evaluacion/detail'),
    path('formularios/pagar',marcar_informe_pagado),
    path('formularios/detalle/<int:pk>', FormulariosDetail.as_view(template_name = "formularios/detail.html"),name='formularios/detalle'),
    path('formularios/cerrar',cerrar_formulario),
    path('formularios/procesar',procesar_diferencias_formulario),
    path('materiales/agregar/', MaterialesCreate.as_view(template_name = "materiales/create.html"),name='materiales'),
    path('materiales/verificar/', Materiales_RecibidosCreate.as_view(template_name = "materiales/create.html"),name='materiales_recibidos'),
    path('punto_recoleccion/listar/', Punto_recoleccionList.as_view(template_name = "puntos_recoleccion/index.html"), name='puntos_recoleccion'),
    path('punto_recoleccion/agregar/', Punto_recoleccionCreate.as_view(template_name = "puntos_recoleccion/create.html")),
    path('punto_recoleccion/listar/recicladores/', RecicladoresList.as_view(template_name = "recicladores/index.html"), name='recicladores'),
    path('punto_recoleccion/listar/recicladores/borrado',destroy_reciclador_punto),
    path('punto_recoleccion/listar/verificar/',verificar_punto),
    path('puntos_recoleccion/',Punto_recoleccion_recicladorList.as_view(template_name = "puntos_recoleccion/index.html")),

    path('recicladores/agregar', UsuariosList.as_view(template_name = "puntos_recoleccion/anidate.html"), name='anidate'),
    path('recicladores/crear',create_reciclador_punto), #pivot e/ reciclador y punto

    path('accounts/login/',LoginView.as_view()),
    path('accounts/logout/',LogoutView.as_view(), name='logout'),

    path('admin/', admin.site.urls),

    # API URLS
    path('api/ordenes_disponibles/', OrdenesList.as_view(), name='ordenes_list'),
    path('api/reservar_orden/<int:pk>/', OrdenReservaUpdate.as_view(), name='orden_reserva_update'),
    path('api/entregar_orden/<int:pk>/', OrdenEntregaUpdate.as_view(), name='orden_entrega_update'),
    path('api/registrar_deposito/', PuntoMaterialRegistro.as_view(), name='punto_material_registro'),

    # API - JWT Tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
