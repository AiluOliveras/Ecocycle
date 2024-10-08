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
from eco.views import MaterialesCreate, FormulariosDetail, FormulariosCreate, cerrar_formulario
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('bienvenida/', include('eco.urls')),

    path('home/', LoginView.as_view()),
    
    path('inicio/', FormulariosCreate.as_view(template_name = "formularios/create.html"),name='inicio'),
    path('formularios/detalle/<int:pk>', FormulariosDetail.as_view(template_name = "formularios/detail.html"),name='formularios/detalle'),
    path('formularios/cerrar',cerrar_formulario),
    path('materiales/agregar/', MaterialesCreate.as_view(template_name = "materiales/create.html"),name='materiales'),

    path('accounts/login/',LoginView.as_view()),

    path('admin/', admin.site.urls),
]
