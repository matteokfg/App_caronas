from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Motorista, Carona, Localizacao

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'cpf_user', 'relation_with_uniso_user', 'genero_user', 'eh_motorista']

    def clean(self):
        data = self.cleaned_data
        pass

class MotoristaForm(forms.ModelForm):
    class Meta:
        model = Motorista
        fields = ['profile', 'foto_motorista', 'foto_carro', 'foto_cnh', 'placa']

    def clean(self):
        data = self.cleaned_data
        pass

class UpdateProfileToMotoristaForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['eh_motorista']

class CaronaForm(forms.ModelForm):
    class Meta:
        model = Carona
        fields = ['motorista', 'inicial_location', 'location_final', 'lotation', 'date_inicial_carona', 'date_final_carona']

    def clean(self):
        data = self.cleaned_data
        pass

class LocalizacaoForm(forms.ModelForm):
    class Meta:
        model = Localizacao
        fields =['latitude', 'longitude']

    def clean(self):
        data = self.cleaned_data
        pass