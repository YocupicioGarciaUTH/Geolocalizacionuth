from django.shortcuts import render

def mapa_bibliotecas(request):
    """
    Vista que muestra el mapa de bibliotecas
    """
    return render(request, 'libros/mapa.html')