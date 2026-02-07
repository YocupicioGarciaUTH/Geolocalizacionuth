from rest_framework import serializers
from .models import Biblioteca

class BibliotecaSerializer(serializers.ModelSerializer):
    """
    Serializer para convertir el modelo Biblioteca a JSON
    
    ¿Qué hace?
    - Convierte objetos Python → JSON (para enviar al frontend)
    - Convierte JSON → objetos Python (cuando recibe datos del frontend)
    """
    
    # Campo adicional calculado automáticamente
    direccion_completa = serializers.CharField(read_only=True)
    
    class Meta:
        model = Biblioteca  # ¿Qué modelo serializar?
        fields = '__all__'  # Incluir todos los campos del modelo
        
        # Campos que no se pueden editar (se calculan automáticamente)
        read_only_fields = ['latitud', 'longitud', 'place_id']
    
    def create(self, validated_data):
        """
        Se ejecuta cuando se crea una nueva biblioteca
        
        1. Crea la biblioteca en la base de datos
        2. Llama a geocodificar() para obtener las coordenadas
        3. Retorna la biblioteca con coordenadas
        """
        biblioteca = super().create(validated_data)  # Crear en BD
        biblioteca.geocodificar()  # Obtener coordenadas de Google Maps
        return biblioteca