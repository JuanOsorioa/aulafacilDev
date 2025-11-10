from django.contrib import admin

# Register your models here.
# principal/admin.py

from django.contrib import admin
# Importamos todas las clases que tienes en models.py
from .models import Aula, Recurso, Reserva, Usuario 

# Registramos cada una de las tablas para que aparezcan en /admin/
admin.site.register(Aula)
admin.site.register(Recurso)
admin.site.register(Reserva)
admin.site.register(Usuario)