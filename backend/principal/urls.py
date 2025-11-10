# principal/urls.py

from django.urls import path
from . import views

# Aquí definiremos las rutas específicas de la aplicación 'principal'
urlpatterns = [
    path('', views.inicio, name='inicio'), # Ejemplo de la vista 'inicio'
]