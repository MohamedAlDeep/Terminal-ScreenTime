# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['screentime_main.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'pandas',
        'psutil',
        'screentime_tracker',
        'screentime_cli'
    ],
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
    name='screentime-tracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Create an app bundle for macOS
app = BUNDLE(
    exe,
    name='ScreenTimeTracker.app',
    icon=None,
    bundle_identifier='com.screentime.tracker',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'NSAppleEventsUsageDescription': 'This app uses AppleScript to track active applications.',
        'NSSystemAdministrationUsageDescription': 'This app needs system access to monitor screen time.',
    },
)
