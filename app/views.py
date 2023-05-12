from django.shortcuts import render
from django.utils import timezone
from .models import Carona
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model

#This file defines the view functions for the app. View functions are Python functions that handle HTTP requests and return HTTP responses. 
#In this file, we define a single view function called 'caronas_disp'. This function takes a request object as its argument and returns a rendered HTML template using the 'render' shortcut function. The rendered template is the 'index.html' template located in the 'app' directory.
#View functions are an essential part of any Django project, as they define the behavior of our web application's pages. By defining view functions in this file, we can ensure that our app responds correctly to incoming requests and provides a consistent user experience.

def inicio_index(request):
    return render(request, 'app/index.html', {})

def caronas_disponiveis(request):
    caronas = Carona.objects.all() #Carona.objects.all().filter(date_final_carona__lte=timezone.now(), date_inicial_carona__gte=timezone.now()-datetime.timedelta(minutes=30)) <- caronas acontecendo agora e comecadas com 30 minutos antes
    return render(request, 'app/caronas_disponiveis.html', {'caronas': caronas})

def cadastro_passageiro(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    
    if request.method == 'POST':
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            user_model = get_user_model()
            user = user_model.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('caronas_disponiveis'))

        # return HttpResponseRedirect(reverse('caronas_disponiveis'))
    
    return render(request, 'app/cadastro_passageiro.html', {})

def cadastro_motorista(request):
    return render(request, 'app/cadastro_motorista.html', {})

def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('caronas_disponiveis'))

    return render(request, 'app/login.html', {})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# @login_required
# def caronas_disponiveis_inicio(request):
#     return HttpResponseRedirect(
#                reverse('caronas_disponiveis', 
#                        args=[request.user.username]))
