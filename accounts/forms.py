from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class NewUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("email", "user_name", "password1", "password2",)
        labels = {
            "email": 'Correo electrónico',
            "user_name": 'Nombre de usuario',
            "password1": 'Contraseña',
            "password2": 'Repita su contraseña'
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label=_("Email"))

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'about',]
        labels = {'about': 'Algo sobre ti', 'first_name': 'Nombre', 'last_name':'Apellidos'}
        widgets = {'about': forms.Textarea(attrs={'cols':80, 'rows':10})}

    

    
