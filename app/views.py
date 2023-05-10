from django.shortcuts import render
from django.utils import timezone
from .models import Carona
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#This file defines the view functions for the app. View functions are Python functions that handle HTTP requests and return HTTP responses. 
#In this file, we define a single view function called 'caronas_disp'. This function takes a request object as its argument and returns a rendered HTML template using the 'render' shortcut function. The rendered template is the 'index.html' template located in the 'app' directory.
#View functions are an essential part of any Django project, as they define the behavior of our web application's pages. By defining view functions in this file, we can ensure that our app responds correctly to incoming requests and provides a consistent user experience.

def inicio_index(request):
    return render(request, 'app/index.html', {})

def caronas_disponiveis(request):
    caronas = Carona.objects.all() #Carona.objects.all().filter(date_final_carona__lte=timezone.now(), date_inicial_carona__gte=timezone.now()-datetime.timedelta(minutes=30)) <- caronas acontecendo agora e comecadas com 30 minutos antes
    return render(request, 'app/caronas_disponiveis.html', {'caronas': caronas})

def cadastro_passageiro(request):
    return render(request, 'app/cadastro_passageiro.html', {})

def cadastro_motorista(request):
    return render(request, 'app/cadastro_motorista.html', {})

def login(request):
    return render(request, 'app/login.html', {})

@login_required
def caronas_disponiveis_inicio(request):
    return HttpResponseRedirect(
               reverse('caronas_disponiveis', 
                       args=[request.user.username]))
