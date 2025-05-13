from django import forms
from .models import Contacto

class PizzaForm(forms.ModelForm):
     class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'mensaje']

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
