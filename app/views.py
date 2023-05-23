from django.shortcuts import render
from django.utils import timezone
from .models import Carona, Motorista, User, Profile, Localizacao
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, ProfileForm, MotoristaForm, CaronaForm, LocalizacaoForm, UpdateProfileToMotoristaForm, UpdateUserForm, UpdateProfileForm, UpdateMotoristaForm
# alterar senha
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

def inicio_index(request):
    return render(request, 'app/index.html', {})


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

@login_required
def caronas_disponiveis(request):
    profile = Profile.objects.get(user_id=request.user.id)

    caronas = list(Carona.objects.all()) #Carona.objects.all().filter(date_final_carona__lte=timezone.now(), date_inicial_carona__gte=timezone.now()-datetime.timedelta(minutes=30)) <- caronas acontecendo agora e comecadas com 30 minutos antes

    context = {
        'caronas': caronas,
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

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
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
            form_profile.save()
            return HttpResponseRedirect(reverse('caronas_disponiveis'))
    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, 'app/cadastro_passageiro.html', {'profile_form': profile_form})

@login_required
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

@login_required
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

@login_required
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

@login_required
def adicionar_localizacao(request):
    if request.method == 'POST':
        locali_form = LocalizacaoForm(request.POST)

        if locali_form.is_valid():
            locali_form.save()
            return HttpResponseRedirect(reverse('adicionar_carona'))
    else:
        locali_form = LocalizacaoForm()

    return render(request, 'app/adicionar_localizacao.html', {'locali_form': locali_form})

@login_required
def atualizar_dados(request):
    profile = Profile.objects.get(user_id=request.user.id)
    motorista = Motorista.objects.get(profile_id=profile.id)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, instance=profile)
        motorista_form = UpdateMotoristaForm(request.POST, instance=motorista)

        if user_form.is_valid():
            user_form.save()

        if profile_form.is_valid():
            profile_form.save()

        if motorista_form.is_valid():
            motorista_form.save()
        if user_form.is_valid() or profile_form.is_valid() or motorista_form.is_valid():
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('caronas_disponiveis'))
        
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=profile)
        motorista_form = UpdateMotoristaForm(instance=motorista)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'motorista_form': motorista_form,
        'profile': profile,
    }
    return render(request, 'app/atualizar_dados.html', context)

@login_required
def alterar_senha(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        form_alterar_senha = PasswordChangeForm(request.user, request.POST)
        if form_alterar_senha.is_valid():
            user = form_alterar_senha.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse('caronas_disponiveis'))
    else:
        form_alterar_senha = PasswordChangeForm(request.user)

    context = {
        'form_alterar_senha': form_alterar_senha,
        'profile': profile,
    }
    return render(request, 'app/alterar_senha.html', context)