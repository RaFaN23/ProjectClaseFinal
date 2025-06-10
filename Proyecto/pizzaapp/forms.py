from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Contacto, Usuario, Pedido, LineaPedido, resena, Reserva


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'mensaje']


class RegistroFormulario(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'apellidos', 'password']


class LoginFormulario(AuthenticationForm):
    username = forms.EmailField(label="Correo electronico")
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


class EmpleadoForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellidos', 'rol', 'password']


class Meta:
    model = Usuario
    fields = ['email', 'password']
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


class PedidoForm(forms.ModelForm):
    class Meta:
        model = LineaPedido
        fields = ['pedido', 'producto', 'cantidad', 'precio']




class form_resena(forms.ModelForm):
    puntuacion = forms.IntegerField(min_value=1,max_value=5,label="Puntuación (1 a 5)")
    comentario = forms.CharField(widget=forms.Textarea,label="Comentario")

    class Meta:
        model = resena
        fields = ['puntuacion', 'comentario']  # usuario se asigna en la vista



class reservaForm(forms.ModelForm):
    numero_personas = forms.IntegerField(min_value=1, max_value=20, label="Numero de personas")
    class Meta:
        model = Reserva

        fields = ['fecha_reserva', 'hora_reserva', 'numero_personas']
        widgets = {
            'fecha_reserva': forms.DateInput(attrs={'type': 'date'}),
            'hora_reserva': forms.TimeInput(attrs={'type': 'time'}),
        }


#
# widgets = {
#     # 📅 Selector de fecha
#     'fecha_reserva': forms.DateInput(
#         attrs={'type': 'date', 'class': 'form-control'}
#     ),  # Para seleccionar una fecha (usa calendario del navegador)
#
#     # 🕒 Selector de hora
#     'hora_reserva': forms.TimeInput(
#         attrs={'type': 'time', 'class': 'form-control'}
#     ),  # Para seleccionar hora exacta
#
#     # 🔡 Campo de texto normal
#     'nombre': forms.TextInput(
#         attrs={'placeholder': 'Tu nombre completo', 'class': 'form-control'}
#     ),  # Para nombres, títulos o texto corto
#
#     # ✉️ Campo de email
#     'correo': forms.EmailInput(
#         attrs={'placeholder': 'ejemplo@correo.com', 'class': 'form-control'}
#     ),  # Valida formato de email automáticamente
#
#     # 🔒 Campo de contraseña
#     'contrasena': forms.PasswordInput(
#         attrs={'class': 'form-control'}
#     ),  # Oculta el texto al escribir
#
#     # 🧾 Área de texto para comentarios o descripciones
#     'comentario': forms.Textarea(
#         attrs={'rows': 4, 'cols': 40, 'placeholder': 'Escribe tu mensaje...', 'class': 'form-control'}
#     ),  # Para escribir textos largos
#
#     # 🔢 Campo numérico
#     'numero_personas': forms.NumberInput(
#         attrs={'min': 1, 'max': 20, 'class': 'form-control'}
#     ),  # Solo permite números dentro del rango
#
#     # 📂 Subida de archivo
#     'imagen': forms.ClearableFileInput(
#         attrs={'class': 'form-control-file'}
#     ),  # Para subir imágenes, permite eliminar si ya hay una
#
#     # ✅ Casilla de verificación
#     'acepta_terminos': forms.CheckboxInput(
#         attrs={'class': 'form-check-input'}
#     ),  # Ideal para aceptar términos y condiciones
#
#     # 🔽 Menú desplegable (solo una opción)
#     'tipo_reserva': forms.Select(
#         attrs={'class': 'form-select'}
#     ),  # Úsalo si tienes un `choices=` en el modelo
#
#     # 🔘 Botones de radio (una sola opción)
#     'opciones_pago': forms.RadioSelect(
#         attrs={'class': 'form-check-input'}
#     ),  # Otra forma visual de elegir una opción
#
#     # 🔽🔍 ComboBox (desplegable con búsqueda)
#     'categoria': forms.Select(
#         attrs={
#             'class': 'form-select select2'  # Usa Select2 (requiere JS y jQuery) para búsqueda
#         }
#     ),  # Para elegir de una lista larga (ej. ciudades, categorías)
# }
#
#
#
# class ReservaForm(forms.ModelForm):
#     class Meta:
#         model = Reserva
#         fields = ['estado', 'numero_personas', 'fecha_reserva', 'hora_reserva']
#         widgets = {
#             'fecha_reserva': forms.DateInput(attrs={'type': 'date'}),
#             'hora_reserva': forms.TimeInput(attrs={'type': 'time'}),
# #         }
# su view
# def crear_reserva(request):
#     reserva_obj = None  # En este caso solo se crea, no se edita
#
#     if request.method == 'POST':
#         form = ReservaForm(request.POST, instance=reserva_obj)
#         if form.is_valid():
#             nueva_reserva = form.save(commit=False)
#             nueva_reserva.usuario = request.user  # Asumiendo que usas autenticación
#             nueva_reserva.save()
#             return redirect('reserva_exitosa')  # Redirige a donde necesites
#     else:
#         form = ReservaForm(instance=reserva_obj)
#
#     contexto = {
#         'form': form,
#         'es_edicion': reserva_obj is not None
#     }
#     return render(request, 'reservas/crear_reserva.html', contexto)