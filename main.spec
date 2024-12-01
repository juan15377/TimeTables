# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
from PyInstaller import *  # Esto incluye todos los módulos de PyInstaller

# Aquí defines las rutas
a = Analysis(
    ['src/main.py'],  # La ruta principal de tu script
    pathex=['/home/juan/GitHub/TimeTables/src'],  # Ruta del proyecto (ajustar si es necesario)
    binaries=[],  # Aquí puedes añadir binarios si es necesario
    datas=collect_data_files('flet'),  # Esto incluye los archivos necesarios de Flet
    hiddenimports=[],  # Si tienes imports ocultos (necesarios para Flet u otras librerías)
    hookspath=[],  # Si tienes hooks personalizados, añádelos aquí
    runtime_hooks=[],  # Hooks en tiempo de ejecución
    excludes=[],  # Si quieres excluir algún módulo que no necesites
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)  # Empaquetar los archivos Python puros

# Definir la creación del archivo ejecutable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',  # Nombre del ejecutable
    debug=False,  # Activar para depuración si es necesario
    bootloader_ignore_signals=False,
    strip=False,  # Si quieres quitar información de depuración
    upx=True,  # Habilitar UPX para comprimir el ejecutable
    upx_exclude=[],  # Archivos que no se deben comprimir con UPX
    runtime_tmpdir=None,
    console=True,  # Mostrar la consola (si tu aplicación es de consola)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
