from django.shortcuts import render

# Create your views here.


def go_home(request):
    return render(request, 'home.html')
    
def go_registro(request):
    return render(request, 'registro_tarjeta.html')

def go_pedido(request):
    return render(request, 'hacer_pedido.html')
