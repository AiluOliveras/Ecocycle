from django.db import models
from django.forms import ModelForm, DateInput
from django import forms
from .models import Materiales, Tiposmateriales
from django import forms
#from django.contrib.auth.models import User

class MaterialesForm(ModelForm):

    class Meta:
        model = Materiales
        fields = ['cantidad', 'tipo']


class TiposmaterialesForm(ModelForm):

    class Meta:
        model = Tiposmateriales
        fields = ['nombre']