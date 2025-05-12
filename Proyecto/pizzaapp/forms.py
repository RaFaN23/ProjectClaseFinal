from django import forms

class PizzaForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Tu nombre")
    email = forms.CharField(max_length=100, label="Tu apellido")
    mensaje = forms.CharField(widget=forms.Textarea, label="Mensaje")
