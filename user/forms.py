from django import forms
from .models import Profil
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #suppression des help_text
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text=''
        self.fields['password2'].help_text = ''



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['address', 'phone', 'image']