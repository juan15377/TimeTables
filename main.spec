# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src/__main__.py'],
    pathex=['/home/juan/GitHub/TimeTables/src'],  # Ruta donde están los archivos fuente
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Deshabilitado UPX para evitar posibles problemas
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Mantén la consola para salida estándar
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
