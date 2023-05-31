# renderizacao de tela com contexto
from django.shortcuts import render
# timezone
from django.utils import timezone
# models, BD
from .models import Carona, Motorista, User, Profile, Localizacao
# redirecionamento de telas
from django.http import HttpResponseRedirect
from django.urls import reverse
# autenticacao, login, logout e necessario login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# forms, create e update
from .forms import UserForm, ProfileForm, MotoristaForm, CaronaForm, LocalizacaoForm, UpdateProfileToMotoristaForm, UpdateUserForm, UpdateProfileForm, UpdateMotoristaForm
# alterar senha
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# view do index
def inicio_index(request):
    return render(request, 'app/index.html', {})  # renderizacao da tela de inicio, sem contexto

# view de cadastro do usuario
def cadastro(request):
    if request.user.is_authenticated:                                   # verifica se a sessão é de um usuario logado
        return HttpResponseRedirect(reverse('caronas_disponiveis'))     # se for, permite que ele entre na pagina de cadastro, redirecionando para a tela de caronas disponiveis

    user_form = UserForm(request.POST or None)                          # cria a um objeto da classe UserForm, se for um POST do form, cria usando os dados do formulario, senao, cria um vazio
    # passa o objeto form como contexto
    context = {
        "user_form": user_form,
    }
    if user_form.is_valid():                                            # se for um POST, verifica se os dados sao validos
        user_object = user_form.save()                                  # se forem, sava os dados
        context['user_form'] = UserForm()                               # esvazia o objeto form do contexto
        login(request, user_object)                                     # faz login
        return HttpResponseRedirect(reverse('cadastro_passageiro'))     # redireciona para a tela de cadastro passageiro

    return render(request, 'app/cadastro_user.html', context=context)   # retorna a tela de cadastro user, com o contexto, que vai ser renderizado

# view da tela de login
def login_user(request):
    if request.user.is_authenticated:                                       # verifica se ja foi feito o login
        return HttpResponseRedirect(reverse('caronas_disponiveis'))         # se ja, nao permite a entrada na tela, redirecionando para a tela de caronas disponiveis

    if request.method == 'POST':                                            # se o verbo Http for POST
        # pega as informacoes de username e senha do formulario
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)  # faz a autenticacao do user
        if user is not None:                                                # se ele existir
            login(request, user)                                            # faz o login
            return HttpResponseRedirect(reverse('caronas_disponiveis'))     # redireciona para a tela de caronas disponiveis

    return render(request, 'app/login.html', {})                            # se nao for o verbo Http Post, renderiza a tela de login

# view da tela de caronas disponiveis
@login_required
def caronas_disponiveis(request):
    profile = Profile.objects.get(user_id=request.user.id)           # faz uma query no BD pelo profile com relacionado com o user logado
    caronas = list(Carona.objects.all())                             # faz a query que pega as caronas no banco de dados
    #Carona.objects.all().filter(date_final_carona__lte=timezone.now(), date_inicial_carona__gte=timezone.now()-datetime.timedelta(minutes=30)) <- caronas acontecendo agora e comecadas com 30 minutos antes

    # dicionario que vai passar as informacoes necessarias para a renderizacao, nessa tela: profile e caronas
    context = {
        'caronas': caronas,
        'profile': profile,
    }
    return render(request, 'app/caronas_disponiveis.html', context)  # renderizacao da tela de caronas disponiveis, passando o contexto

# view de logout
@login_required
def logout_user(request):
    logout(request)                                 # faz logout do user
    return HttpResponseRedirect(reverse('index'))   # redireciona para a tela inicial

# view de cadastro de passageiro
@login_required
def cadastro_passageiro(request):
    profile = Profile.objects.get(user_id=request.user.id)                                  # faz uma query no BD pelo profile com relacionado com o user logado

    if request.method == 'POST':                                                            # verifica se o verbo Http e Post
        profile_form = ProfileForm(request.POST, instance=profile)                          # cria o objeto form, com as informacoes do formulario e do BD

        if profile_form.is_valid():                                                         # verifica se os dados sao validos
            form_profile = profile_form.save(commit=False)                                  # salva os dados mas ainda nao para o BD
            ehs_motorista = form_profile.eh_motorista                                       # pega o valor de e eh_motorista
            if ehs_motorista:                                                               # verifica se o usuario e motorista
                form_profile.save()                                                         # salva o form
                return HttpResponseRedirect(reverse('cadastro_motorista'))                  # redireciona para o cadastro de motorista
            form_profile.save()                                                             # salva o form
            return HttpResponseRedirect(reverse('caronas_disponiveis'))                     # redireiciona para as caronas disponiveis
    else: # se for Get
        profile_form = ProfileForm(instance=profile)                                        # cria o form, com as informacoes do BD

    return render(request, 'app/cadastro_passageiro.html', {'profile_form': profile_form})  # renderiza a tela de cadastro de motorista, com o contexto

# view do cadastro de mudanca de persona passagiero para motorista
@login_required
def passageiro_to_motorista(request):
    profile = Profile.objects.get(user_id=request.user.id)                                          # faz uma query no BD pelo profile com relacionado com o user logado

    if request.method == 'POST':                                                                    # se for Post
        update_profile_to_motorista = UpdateProfileToMotoristaForm(request.POST, instance=profile)  # cria form com dados de Psot e BD
        if update_profile_to_motorista.is_valid():                                                  # verifica se e valido
            update_profile = update_profile_to_motorista.save(commit=False)                         # salva as mudancas, mas ainda nao no BD
            quer_ser = update_profile.eh_motorista                                                  # pega o dado eh_motorista
            if quer_ser:                                                                            # se quiser ser
                update_profile_to_motorista.save()                                                  # salva as mudancas no BD
                return HttpResponseRedirect(reverse('cadastro_motorista'))                          # e redireciona para a tela de cadastro de motorista
            return HttpResponseRedirect(reverse('caronas_disponiveis'))                             # redireciona para a tela de caronas disponiveis

    else:                                                                                           # se for Get
        update_profile_to_motorista = UpdateProfileToMotoristaForm(instance=profile)                # cria o form com os dados do BD

    # passa como contexto o form e profile
    context = {
        'profile_motorista_update_form' : update_profile_to_motorista,
        'profile': profile,
    }

    return render(request, 'app/ser_motorista.html', context)                                       # renderiza a tela de mudanca de persona de passageiro para motorista

# view de cadastro de motorista
@login_required
def cadastro_motorista(request):
    profile = Profile.objects.get(user_id=request.user.id)                                  # faz uma query no BD pelo profile relacionado com o user logado
    motorista = Motorista.objects.get(profile_id=profile.id)                                # faz uma query no BD pelo motorista relacionado com o profile logado

    if motorista.foto_motorista:                                                            # se o usuario ja estiver cadastrado como motorista
        return HttpResponseRedirect(reverse('caronas_disponiveis'))                         # redireciona para a tela de caronas disponiveis

    if request.method == 'POST':                                                            # se for Post
        motorista_form = MotoristaForm(request.POST, request.FILES,  instance=motorista)    # cria o form, com as informacoes do POST, os arquivos e os dados de BD

        if motorista_form.is_valid():                                                       # verifica se o form e valido
            motorista_form.save()                                                           # salva o form
            return HttpResponseRedirect(reverse('caronas_disponiveis'))                     # redireciona para a tela de caronas disponiveis
    else:                                                                                   # se for Get
        motorista_form = MotoristaForm(instance=motorista)                                  # cria o form com os dados do BD

    # contexto com form e profile
    context = {
        'motorista_form': motorista_form,
        'profile': profile,
    }
    
    return render(request, 'app/cadastro_motorista.html', context)                          # renderizacoa da tela de cadastro do motorista e contexto

# view de adicionar carona
@login_required
def adicionar_carona(request):
    profile = Profile.objects.get(user_id= request.user.id)             # faz uma query no BD pelo profile relacionado com o user logado
    motorista = Motorista.objects.get(profile_id=profile.id)            # faz uma query no BD pelo motorista relacionado com o profile logado

    if not (bool(motorista.foto_motorista) != False):                   # se o motorista nao terminou o cadastro
        return HttpResponseRedirect(reverse('caronas_disponiveis'))     # e redirecioado para caronas disponiveis

    
    carona_form = CaronaForm(request.POST or None)                      # cria form da carona

    # contexto com form, motorista e profile
    context = {
        'carona_form': carona_form,
        'motorista': motorista,
        'profile': profile,
    }

    if carona_form.is_valid():                                          # verifica se o form e valido e "Post"
        carona = carona_form.save(commit=False)                         # salva mas ainda nao no BD
        carona.motorista_id = motorista.id                              # modifica o campo motorista id, para ser o mesmo do motorista logado
        carona.save()                                                   # salva no BD

        context['carona_form'] = CaronaForm()                           # esvazia o form
        return HttpResponseRedirect(reverse('caronas_disponiveis'))     # redireciona para caronas disponiveis

    return render(request, 'app/adicionar_carona.html', context)        # renderiza a tela de adicionar carona, com o contexto

# view adicionar localizacao
@login_required
def adicionar_localizacao(request):
    profile = Profile.objects.get(user_id= request.user.id)             # faz uma query no BD pelo profile relacionado com o user logado
    motorista = Motorista.objects.get(profile_id=profile.id)            # faz uma query no BD pelo motorista relacionado com o profile logado

    if not (bool(motorista.foto_motorista) != False):                   # se o motorista nao terminou o cadastro
        return HttpResponseRedirect(reverse('caronas_disponiveis'))     # e redirecioado para caronas disponiveis

    if request.method == 'POST':                                        # se for Post
        locali_form = LocalizacaoForm(request.POST)                     # cria form com dados do Post

        if locali_form.is_valid():                                      # verifica se o form e valido
            locali_form.save()                                          # salva o form no BD
            return HttpResponseRedirect(reverse('adicionar_carona'))    # redireciona para adicionar carona
    else:                                                               # se for Get
        locali_form = LocalizacaoForm()                                 # form vazio

    # contexto com form e profile
    context = {
        'locali_form': locali_form,
        'profile': profile,
    }
    return render(request, 'app/adicionar_localizacao.html', context)  # renderizacao da tela adicionar localizacao, com contexto

# view atualizar dados cadastrais
@login_required
def atualizar_dados(request):
    profile = Profile.objects.get(user_id=request.user.id)                  # faz uma query no BD pelo profile relacionado com o user logado
    motorista = Motorista.objects.get(profile_id=profile.id)                # faz uma query no BD pelo motorista relacionado com o profile logado

    if request.method == 'POST':                                                                # ser for Post
        user_form = UpdateUserForm(request.POST, instance=request.user)                         # cria form de User, com dados do Post e do BD
        profile_form = UpdateProfileForm(request.POST, instance=profile)                        # cria form de Profile, com dados do Post e do BD
        motorista_form = UpdateMotoristaForm(request.POST, request.FILES, instance=motorista)   # cria form de Motorista, com dados do Post, dos arquivos e do BD

        if user_form.is_valid():                    # verifica se o form User e valido
            user_form.save()                        # salva o form User

        if profile_form.is_valid():                 # verifica se o form Profile e valido
            profile_form.save()                     # salva o form Profile

        if motorista_form.is_valid():               # verifica se o form Motorista e valido
            motorista_form.save()                   # salva o form Motorista

        if user_form.is_valid() or profile_form.is_valid() or motorista_form.is_valid():    # como o usuario pode apenas ter alterado um form, "or" para as validacoes dos forms
            return HttpResponseRedirect(reverse('caronas_disponiveis'))                     # redireciona para a tela caronas disponiveis

    else:                                                           # se for Get
        user_form = UpdateUserForm(instance=request.user)           # cria form User com os dados do BD
        profile_form = UpdateProfileForm(instance=profile)          # cria form Profile com dados do BD
        motorista_form = UpdateMotoristaForm(instance=motorista)    # cria form Motorista com dados do BD

    # contexto com forms e profile
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'motorista_form': motorista_form,
        'profile': profile,
    }
    return render(request, 'app/atualizar_dados.html', context)     # renderizacao da tela alterar dados, com contexto

# view alterar senha
@login_required
def alterar_senha(request):
    profile = Profile.objects.get(user_id=request.user.id)      # faz uma query no BD pelo profile relacionado com o user logado
    if request.method == 'POST':                                                # se for Post
        form_alterar_senha = PasswordChangeForm(request.user, request.POST)     # cria form para alterar senha, com dados do Post e do User logado
        if form_alterar_senha.is_valid():                                       # verifica se e valido
            user = form_alterar_senha.save()                                    # salva no BD
            update_session_auth_hash(request, user)                             # atualiza a sessao com o hash da nova senha
            return HttpResponseRedirect(reverse('caronas_disponiveis'))         # redireciona para a tela de caronas disponiveis
    else:                                                                       # se for Get
        form_alterar_senha = PasswordChangeForm(request.user)                   # cria form para alterar senha, com dados do user logado

    # contexto com form e profile
    context = {
        'form_alterar_senha': form_alterar_senha,
        'profile': profile,
    }
    return render(request, 'app/alterar_senha.html', context)                   # renderizacao da tela alterar senha, com contexto