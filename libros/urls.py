from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import BibliotecaViewSet
from .views import mapa_bibliotecas  # ⭐ Importar la vista

router = DefaultRouter()
router.register(r'bibliotecas', BibliotecaViewSet, basename='biblioteca')

urlpatterns = [
    path('', include(router.urls)),
    path('mapa/', mapa_bibliotecas, name='mapa'),  # ⭐ Ruta del mapa
]