import os

def crear_estructura(directorio_base):
    # Crear la carpeta principal si no existe
    if not os.path.exists(directorio_base):
        os.makedirs(directorio_base)
    
    # Crear subcarpetas dentro del directorio base
    subcarpetas = ['subcarpeta1', 'subcarpeta2']
    for sub in subcarpetas:
        os.makedirs(os.path.join(directorio_base, sub), exist_ok=True)

# Ejemplo de uso
nombre_directorio = "/home/juan/Escritorio/HOLA_GUAPO"
crear_estructura(nombre_directorio)
