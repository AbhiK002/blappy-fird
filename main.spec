# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
    	('assets\\pillars\\1_pillar_down.png', '.\\assets\\pillars'),
    	('assets\\pillars\\1_pillar_up.png', '.\\assets\\pillars'),
    	('assets\\birds\\1_bird.png', '.\\assets\\birds'),
    	('assets\\bg\\1_skybg.png', '.\\assets\\bg'),
    	('assets\\*.png', '.\\assets')
#    	('assets\play.png', 'assets'),
#    	('assets\help.png', 'assets'),
#    	('assets\logo.png', 'assets')
    	],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['bflogo.ico'],
)
