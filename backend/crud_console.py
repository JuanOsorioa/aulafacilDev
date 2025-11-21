import os
import django
import sys
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aulafacil.settings')
django.setup()

from principal.models import Aula, Recurso, Reserva, Usuario
from django.contrib.auth.hashers import make_password

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("\n" + "=" * 40)
    print(f" {title}")
    print("=" * 40)

def get_input(prompt, required=True):
    while True:
        value = input(f"{prompt}: ").strip()
        if value or not required:
            return value
        print("Este campo es obligatorio.")

# --- Generic CRUD Functions ---

def list_objects(model, fields=None):
    objects = model.objects.all()
    if not objects.exists():
        print("\nNo hay registros.")
        return

    print(f"\nRegistros encontrados ({objects.count()}):")
    # If no fields provided, use all fields from the model
    if not fields:
        headers = [field.name for field in model._meta.fields]
    else:
        headers = fields

    print(" | ".join(headers))
    print("-" * 50)
    
    for obj in objects:
        values = [str(getattr(obj, f)) for f in headers]
        print(" | ".join(values))

def delete_object(model):
    pk_name = model._meta.pk.name
    pk = get_input(f"Ingrese ID ({pk_name}) a eliminar")
    try:
        obj = model.objects.get(pk=pk)
        obj.delete()
        print("Registro eliminado exitosamente.")
    except model.DoesNotExist:
        print("Registro no encontrado.")
    except Exception as e:
        print(f"Error: {e}")

# --- Specific Model Handlers ---

def manage_aula():
    while True:
        print_header("GESTIÓN DE AULAS")
        print("1. Listar")
        print("2. Crear")
        print("3. Actualizar")
        print("4. Eliminar")
        print("0. Volver")
        
        op = input("\nOpción: ")
        
        if op == '0': break
        elif op == '1':
            list_objects(Aula)
        elif op == '2':
            nombre = get_input("Nombre Aula")
            capacidad = get_input("Capacidad")
            desc = get_input("Descripción", required=False)
            try:
                Aula.objects.create(nombre_aula=nombre, capacidad=capacidad, descripcion=desc)
                print("Aula creada.")
            except Exception as e:
                print(f"Error: {e}")
        elif op == '3':
            id_aula = get_input("ID Aula a actualizar")
            try:
                aula = Aula.objects.get(pk=id_aula)
                print(f"Editando: {aula.nombre_aula}")
                aula.nombre_aula = get_input(f"Nombre [{aula.nombre_aula}]", False) or aula.nombre_aula
                cap = get_input(f"Capacidad [{aula.capacidad}]", False)
                if cap: aula.capacidad = cap
                aula.descripcion = get_input(f"Descripción [{aula.descripcion}]", False) or aula.descripcion
                aula.save()
                print("Aula actualizada.")
            except Aula.DoesNotExist:
                print("Aula no encontrada.")
        elif op == '4':
            delete_object(Aula)

def manage_usuario():
    while True:
        print_header("GESTIÓN DE USUARIOS")
        print("1. Listar")
        print("2. Crear")
        print("3. Actualizar")
        print("4. Eliminar")
        print("0. Volver")
        
        op = input("\nOpción: ")
        
        if op == '0': break
        elif op == '1':
            list_objects(Usuario)
        elif op == '2':
            nombre = get_input("Nombre")
            apellido = get_input("Apellido")
            correo = get_input("Correo")
            password = get_input("Contraseña")
            rol = get_input("Rol (estudiante/administrador/profesor)")
            try:
                Usuario.objects.create(
                    nombre=nombre, apellido=apellido, correo=correo,
                    contraseña=make_password(password), rol=rol
                )
                print("Usuario creado.")
            except Exception as e:
                print(f"Error: {e}")
        elif op == '3':
            uid = get_input("ID Usuario a actualizar")
            try:
                u = Usuario.objects.get(pk=uid)
                print(f"Editando: {u.nombre} {u.apellido}")
                u.nombre = get_input(f"Nombre [{u.nombre}]", False) or u.nombre
                u.apellido = get_input(f"Apellido [{u.apellido}]", False) or u.apellido
                u.correo = get_input(f"Correo [{u.correo}]", False) or u.correo
                u.rol = get_input(f"Rol [{u.rol}]", False) or u.rol
                pwd = get_input("Nueva Contraseña (dejar vacío para no cambiar)", False)
                if pwd:
                    u.contraseña = make_password(pwd)
                u.save()
                print("Usuario actualizado.")
            except Usuario.DoesNotExist:
                print("Usuario no encontrado.")
        elif op == '4':
            delete_object(Usuario)

def manage_recurso():
    while True:
        print_header("GESTIÓN DE RECURSOS")
        print("1. Listar")
        print("2. Crear")
        print("3. Actualizar")
        print("4. Eliminar")
        print("0. Volver")
        
        op = input("\nOpción: ")
        
        if op == '0': break
        elif op == '1':
            list_objects(Recurso)
        elif op == '2':
            nombre = get_input("Nombre Recurso")
            tipo = get_input("Tipo")
            estado = get_input("Estado")
            id_aula = get_input("ID Aula")
            try:
                aula = Aula.objects.get(pk=id_aula)
                Recurso.objects.create(nombre_recurso=nombre, tipo=tipo, estado=estado, id_aula=aula)
                print("Recurso creado.")
            except Aula.DoesNotExist:
                print("Aula no existe.")
            except Exception as e:
                print(f"Error: {e}")
        elif op == '3':
            rid = get_input("ID Recurso a actualizar")
            try:
                r = Recurso.objects.get(pk=rid)
                r.nombre_recurso = get_input(f"Nombre [{r.nombre_recurso}]", False) or r.nombre_recurso
                r.tipo = get_input(f"Tipo [{r.tipo}]", False) or r.tipo
                r.estado = get_input(f"Estado [{r.estado}]", False) or r.estado
                
                new_aula = get_input(f"ID Aula [{r.id_aula.id_aula}]", False)
                if new_aula:
                    r.id_aula = Aula.objects.get(pk=new_aula)
                
                r.save()
                print("Recurso actualizado.")
            except Exception as e:
                print(f"Error: {e}")
        elif op == '4':
            delete_object(Recurso)

def manage_reserva():
    while True:
        print_header("GESTIÓN DE RESERVAS")
        print("1. Listar")
        print("2. Crear")
        print("3. Actualizar")
        print("4. Eliminar")
        print("0. Volver")
        
        op = input("\nOpción: ")
        
        if op == '0': break
        elif op == '1':
            list_objects(Reserva)
        elif op == '2':
            inicio = get_input("Inicio (YYYY-MM-DD HH:MM)")
            fin = get_input("Fin (YYYY-MM-DD HH:MM)")
            id_aula = get_input("ID Aula")
            id_usuario = get_input("ID Usuario")
            try:
                aula = Aula.objects.get(pk=id_aula)
                usuario = Usuario.objects.get(pk=id_usuario)
                Reserva.objects.create(
                    inicio=inicio, fin=fin, estado='pendiente',
                    id_aula=aula, id_usuario=usuario
                )
                print("Reserva creada.")
            except Exception as e:
                print(f"Error: {e}")
        elif op == '3':
            rid = get_input("ID Reserva a actualizar")
            try:
                r = Reserva.objects.get(pk=rid)
                r.inicio = get_input(f"Inicio [{r.inicio}]", False) or r.inicio
                r.fin = get_input(f"Fin [{r.fin}]", False) or r.fin
                r.estado = get_input(f"Estado [{r.estado}]", False) or r.estado
                r.save()
                print("Reserva actualizada.")
            except Exception as e:
                print(f"Error: {e}")
        elif op == '4':
            delete_object(Reserva)

def main_menu():
    while True:
        print_header("SISTEMA DE GESTIÓN AULA FACIL - CONSOLA")
        print("1. Gestionar Aulas")
        print("2. Gestionar Usuarios")
        print("3. Gestionar Recursos")
        print("4. Gestionar Reservas")
        print("0. Salir")
        
        op = input("\nSeleccione una opción: ")
        
        if op == '1': manage_aula()
        elif op == '2': manage_usuario()
        elif op == '3': manage_recurso()
        elif op == '4': manage_reserva()
        elif op == '0': 
            print("Adiós!")
            break
        else:
            print("Opción no válida.")

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nOperación cancelada.")
