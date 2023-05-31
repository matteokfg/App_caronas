from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile, Motorista, Carona, Localizacao

# form de criação do User do Django, herdando o UserCreationForm
class UserForm(UserCreationForm):
    class Meta:
        model = User                                                                            # model a ser utilizado: User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']     # fields a serem mostrados

# form de criacao do Profiel, herdando o ModelForm -> serve para transformar os fields do Model em fields de formulario, assim já tendo a validacao dos campos
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile                                                                             # model a ser utilizado: Profile
        fields = ['user', 'cpf_user', 'relation_with_uniso_user', 'genero_user', 'eh_motorista']    # fields a serem mostrados

# form de criacao do Motorista, herdando o ModelForm
class MotoristaForm(forms.ModelForm):
    class Meta:
        model = Motorista                                                           # model a ser utilizado: Motorista
        fields = ['profile', 'foto_motorista', 'foto_carro', 'foto_cnh', 'placa']   # fields a serem mostrados

# form de criacao de uma Carona, herdando o ModelForm
class CaronaForm(forms.ModelForm):
    class Meta:
        model = Carona                                                                                                          # model a ser utilizado: Carona
        fields = ['motorista', 'inicial_location', 'location_final', 'lotation', 'date_inicial_carona', 'date_final_carona']    # fields a serem mostrados

# form de criacao de uma Localizacao, herdando o ModelForm
class LocalizacaoForm(forms.ModelForm):
    class Meta:
        model = Localizacao                 # model a ser utilizado: Localizacao
        fields =['latitude', 'longitude']   # fields a serem mostrados

# form para atualizar o campo eh_motorista de Profile, para fazr cadastro com Motorista, herdando o ModelForm
class UpdateProfileToMotoristaForm(forms.ModelForm):
    class Meta:
        model = Profile             # model a ser utilizado: Profile
        fields = ['eh_motorista']   # field a ser mostrado, e possivelmente alterado o seu valor

# form de Update do User, herdando o UserChangeForm
class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User                                                # model a ser utilizado: User
        fields = ['username', 'first_name', 'last_name', 'email']   # fields a serem mostrados

# form de Update do Profile, herdando o ModelForm
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile                                                                     # model a ser utilizado: Profile
        fields = ['cpf_user', 'relation_with_uniso_user', 'genero_user', 'eh_motorista']    # fields a serem mostrados

# form de Update do Motorista, herdando o ModelForm
class UpdateMotoristaForm(forms.ModelForm):
    class Meta:
        model = Motorista                                                   # model a ser utilizado: Motorista
        fields = ['foto_motorista', 'foto_carro', 'foto_cnh', 'placa']      # fields a serem mostrados
