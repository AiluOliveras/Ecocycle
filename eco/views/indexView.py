from django.shortcuts import render
from django.http import HttpResponse
from ..bonita.access import Access

def index(request):
    return HttpResponse("Proyecto Ecocycle, it's working!! :)")
