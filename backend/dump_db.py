import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aulafacil.settings')
django.setup()

from principal.models import Aula, Recurso, Reserva, Usuario

def print_queryset(name, qs):
    print(f"\n--- {name} ({qs.count()}) ---")
    if not qs.exists():
        print(" (Sin registros)")
        return
    
    # Get all field names
    fields = [field.name for field in qs.model._meta.fields]
    print(" | ".join(fields))
    
    for obj in qs:
        values = [str(getattr(obj, f)) for f in fields]
        print(" | ".join(values))

print("VOLCADO DE BASE DE DATOS")
print_queryset("AULAS", Aula.objects.all())
print_queryset("USUARIOS", Usuario.objects.all())
print_queryset("RECURSOS", Recurso.objects.all())
print_queryset("RESERVAS", Reserva.objects.all())
