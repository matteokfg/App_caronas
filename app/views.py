from django.shortcuts import render
from django.utils import timezone
from .models import Carona, Motorista, User, Profile, Localizacao
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import UserForm, ProfileForm, MotoristaForm, CaronaForm, LocalizacaoForm, UpdateProfileToMotoristaForm

#This file defines the view functions for the app. View functions are Python functions that handle HTTP requests and return HTTP responses. 
#In this file, we define a single view function called 'caronas_disp'. This function takes a request object as its argument and returns a rendered HTML template using the 'render' shortcut function. The rendered template is the 'index.html' template located in the 'app' directory.
#View functions are an essential part of any Django project, as they define the behavior of our web application's pages. By defining view functions in this file, we can ensure that our app responds correctly to incoming requests and provides a consistent user experience.

def inicio_index(request):
    return render(request, 'app/index.html', {})


def caronas_disponiveis(request):
    profile = Profile.objects.get(user_id=request.user.id)
    caronas = Carona.objects.all() #Carona.objects.all().filter(date_final_carona__lte=timezone.now(), date_inicial_carona__gte=timezone.now()-datetime.timedelta(minutes=30)) <- caronas acontecendo agora e comecadas com 30 minutos antes

    caronas_motoristas_id = caronas.values_list('motorista_id', flat=True)
    motoristas = Motorista.objects.filter(id__in=caronas_motoristas_id)

    motoristas_profiles_id = motoristas.values_list('profile_id', flat=True)
    profiles = Profile.objects.filter(id__in=motoristas_profiles_id)

    profiles_users_id = profiles.values_list('user_id', flat=True)
    users = User.objects.filter(id__in=profiles_users_id)


    data_caronas_motoristas_profiles_users = zip(list(caronas), list(motoristas), list(profiles), list(users))

    context = {
        'data_caronas_motoristas_profiles_users': data_caronas_motoristas_profiles_users,
        'profile': profile,
    }
    return render(request, 'app/caronas_disponiveis.html', context)


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


def cadastro(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    user_form = UserForm(request.POST or None)
    context = {
        "user_form": user_form,
    }
    if user_form.is_valid():
        user_object = user_form.save()
        context['user_form'] = UserForm()
        login(request, user_object)
        return HttpResponseRedirect(reverse('cadastro_passageiro'))
    
    return render(request, 'app/cadastro_user.html', context=context)


def cadastro_passageiro(request):
    profile = Profile.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)

        if profile_form.is_valid():
            form_profile = profile_form.save(commit=False)
            ehs_motorista = form_profile.eh_motorista
            if ehs_motorista:
                form_profile.save()
                return HttpResponseRedirect(reverse('cadastro_motorista'))
            return HttpResponseRedirect(reverse('caronas_disponiveis'))
    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, 'app/cadastro_passageiro.html', {'profile_form': profile_form})


def passageiro_to_motorista(request):
    profile = Profile.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        update_profile_to_motorista = UpdateProfileToMotoristaForm(request.POST, instance=profile)
        if update_profile_to_motorista.is_valid():
            update_profile_to_motorista.save()
            return HttpResponseRedirect(reverse('cadastro_motorista'))

    else:
        update_profile_to_motorista = UpdateProfileToMotoristaForm(instance=profile)

    context = {
        'profile_motorista_update_form' : update_profile_to_motorista,
        'profile': profile,
    }

    return render(request, 'app/ser_motorista.html', context)


def cadastro_motorista(request):
    profile = Profile.objects.get(user_id=request.user.id)
    motorista = Motorista.objects.get(profile_id=profile.id)

    if request.method == 'POST':
        motorista_form = MotoristaForm(request.POST, instance=motorista)

        if motorista_form.is_valid():
            motorista_form.save()
            return HttpResponseRedirect(reverse('caronas_disponiveis'))
    else:
        motorista_form = MotoristaForm(instance=motorista)

    context = {
        'motorista_form': motorista_form,
        'profile': profile,
    }
    
    return render(request, 'app/cadastro_motorista.html', context)


def adicionar_carona(request):
    # localizacoes = Localizacao.objects.all()
    profile = Profile.objects.get(user_id= request.user.id)
    motorista = Motorista.objects.get(profile_id=profile.id)
    carona_form = CaronaForm(request.POST or None)
    context = {
        'carona_form': carona_form,
        'motorista': motorista,
        'profile': profile,
        # 'localizacoes': localizacoes,
    }
    if carona_form.is_valid():
        carona = carona_form.save(commit=False)
        carona.motorista_id = motorista.id
        carona.save()

        context['carona_form'] = CaronaForm()
        return HttpResponseRedirect(reverse('caronas_disponiveis'))

    return render(request, 'app/adicionar_carona.html', context)