from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Contacto, Usuario


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'mensaje']


class RegistroFormulario(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'apellidos', 'rol', 'password']


class LoginFormulario(AuthenticationForm):
    username = forms.EmailField(label="Correo electrónico")

    class Meta:
        model = Usuario
        fields = ['email', 'password']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Escribe tu mensaje aquí...'}),
        }
        labels = {
            'nombre': 'Nombre completo',
            'email': 'Correo electrónico',
            'mensaje': 'Mensaje',
        }
        help_texts = {
            'email': 'Usa un correo válido como nombre@ejemplo.com',
        }
