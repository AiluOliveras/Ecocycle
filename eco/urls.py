from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bonita", views.bonita, name="bonita")
]