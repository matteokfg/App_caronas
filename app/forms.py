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
        fields = '__all__'

    def clean(self):
        data = self.cleaned_data
        pass

class CaronaForm(forms.ModelForm):
    class Meta:
        model = Carona
        fields = '__all__'

    def clean(self):
        data = self.cleaned_data
        pass

class LocalizacaoForm(forms.ModelForm):
    class Meta:
        model = Localizacao
        fields = '__all__'

    def clean(self):
        data = self.cleaned_data
        pass