from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Biblioteca
from .serializers import BibliotecaSerializer
from .services import GoogleMapsService

class BibliotecaViewSet(viewsets.ModelViewSet):
    """
    ViewSet que maneja todas las operaciones con Bibliotecas
    
    Endpoints que crea automáticamente:
    - GET    /api/bibliotecas/          → Listar todas
    - POST   /api/bibliotecas/          → Crear nueva
    - GET    /api/bibliotecas/{id}/     → Ver una específica
    - PUT    /api/bibliotecas/{id}/     → Actualizar
    - DELETE /api/bibliotecas/{id}/     → Eliminar
    """
    
    queryset = Biblioteca.objects.all()  # Todas las bibliotecas
    serializer_class = BibliotecaSerializer  # Usar este serializer
    
    # Endpoint personalizado: /api/bibliotecas/cercanas/?lat=14.0723&lng=-87.1921
    @action(detail=False, methods=['get'])
    def cercanas(self, request):
        """
        Obtiene bibliotecas cercanas a una ubicación
        
        Parámetros requeridos:
        - lat: Latitud del usuario
        - lng: Longitud del usuario
        
        Ejemplo: GET /api/bibliotecas/cercanas/?lat=14.0723&lng=-87.1921
        """
        
        # Obtener parámetros de la URL
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        
        # Validar que vengan los parámetros
        if not lat or not lng:
            return Response(
                {'error': 'Se requieren parámetros lat y lng'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filtrar solo bibliotecas con coordenadas
        bibliotecas = self.queryset.filter(
            latitud__isnull=False,
            longitud__isnull=False
        )
        
        # Convertir a JSON y retornar
        serializer = self.get_serializer(bibliotecas, many=True)
        return Response(serializer.data)
    
    # Endpoint personalizado: POST /api/bibliotecas/{id}/geocodificar/
    @action(detail=True, methods=['post'])
    def geocodificar(self, request, pk=None):
        """
        Geocodifica una biblioteca específica manualmente
        
        Ejemplo: POST /api/bibliotecas/1/geocodificar/
        """
        
        biblioteca = self.get_object()  # Obtener la biblioteca por ID
        
        if biblioteca.geocodificar():  # Intentar geocodificar
            return Response({
                'mensaje': 'Geocodificación exitosa',
                'nombre': biblioteca.nombre,
                'latitud': str(biblioteca.latitud),
                'longitud': str(biblioteca.longitud)
            })
        
        return Response(
            {'error': 'No se pudo geocodificar la dirección'},
            status=status.HTTP_400_BAD_REQUEST
        )