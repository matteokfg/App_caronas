from django import forms

from .models import Profile, Motorista, Carona, Localizacao



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

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