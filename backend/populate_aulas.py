import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aulafacil.settings')
django.setup()

from principal.models import Aula

def populate():
    print("Iniciando creación de aulas...")
    aulas_data = [
        {"nombre_aula": "Aula 101", "capacidad": 30, "descripcion": "Aula general planta baja"},
        {"nombre_aula": "Aula 102", "capacidad": 25, "descripcion": "Aula general con proyector"},
        {"nombre_aula": "Laboratorio A", "capacidad": 20, "descripcion": "Laboratorio de computación"},
        {"nombre_aula": "Laboratorio B", "capacidad": 20, "descripcion": "Laboratorio de electrónica"},
        {"nombre_aula": "Auditorio", "capacidad": 100, "descripcion": "Auditorio principal para eventos"},
    ]

    count = 0
    for data in aulas_data:
        aula, created = Aula.objects.get_or_create(
            nombre_aula=data["nombre_aula"],
            defaults={
                "capacidad": data["capacidad"],
                "descripcion": data["descripcion"]
            }
        )
        if created:
            print(f"Creada: {aula.nombre_aula}")
            count += 1
        else:
            print(f"Ya existe: {aula.nombre_aula}")
            
    print(f"\nProceso finalizado. Se crearon {count} aulas nuevas.")

if __name__ == '__main__':
    populate()
