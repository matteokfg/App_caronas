from django.shortcuts import render
from django.utils import timezone
from .models import Carona, Motorista, User, Profile
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import UserForm, ProfileForm, MotoristaForm, CaronaForm, LocalizacaoForm

#This file defines the view functions for the app. View functions are Python functions that handle HTTP requests and return HTTP responses. 
#In this file, we define a single view function called 'caronas_disp'. This function takes a request object as its argument and returns a rendered HTML template using the 'render' shortcut function. The rendered template is the 'index.html' template located in the 'app' directory.
#View functions are an essential part of any Django project, as they define the behavior of our web application's pages. By defining view functions in this file, we can ensure that our app responds correctly to incoming requests and provides a consistent user experience.

def inicio_index(request):
    return render(request, 'app/index.html', {})

def caronas_disponiveis(request):
    caronas = Carona.objects.all() #Carona.objects.all().filter(date_final_carona__lte=timezone.now(), date_inicial_carona__gte=timezone.now()-datetime.timedelta(minutes=30)) <- caronas acontecendo agora e comecadas com 30 minutos antes
    
    caronas_motoristas_id = caronas.values_list('motorista_id', flat=True)
    motoristas = list(Motorista.objects.filter(id__in=caronas_motoristas_id))
    print(motoristas[0].foto_motorista)
    caronas_e_motoristas = zip(list(caronas), motoristas)
    
    return render(request, 'app/caronas_disponiveis.html', {'caronas_e_motoristas': caronas_e_motoristas})

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

def adicionar_carona(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'app/adicionar_carona.html', {})
        if request.method == 'POST':

            return HttpResponseRedirect(reverse('caronas_disponiveis'))
    return HttpResponseRedirect(reverse('index'))

def cadastro_passageiro_antigo(request):
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

#---------------- usando forms.py ----------------------

def cadastro(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    form_user = UserForm(request.POST or None)
    context = {
        "form_user": form_user,
    }
    if form_user.is_valid():
        user_object = form_user.save()
        context['form_user'] = UserForm()
        login(request, user_object)
        return HttpResponseRedirect(reverse('cadastro_passageiro'))
    
    return render(request, 'app/cadastro_user.html', context=context)

def cadastro_passageiro(request):
    profile = Profile.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse('caronas_disponiveis'))
    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, 'app/cadastro_passageiro.html', {'profile_form': profile_form})
    # form_profile = ProfileForm(request.POST or None)
    # context = {
    #     'form_profile': form_profile,
    # }
    # if form_profile.is_valid():
    #     # profile_object = Profile.objects.create(user=request.user, cpf_user=request.POST.get("cpf_user"), relation_with_uniso_user=request.POST.get("relation_with_uniso_user"), genero_user=request.POST.get("genero_user"), eh_motorista=request.POST.get("eh_motorista"))
    #     profile_object = form_profile.save()
    #     context['form_profile'] = ProfileForm()
    #     return HttpResponseRedirect(reverse('caronas_disponiveis'))
    
    # return render(request, 'app/cadastro_passageiro.html', context=context)