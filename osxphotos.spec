# -*- mode: python ; coding: utf-8 -*-
# spec file for pyinstaller
# run `pyinstaller osxphotos.spec`


import importlib
import os

pathex = os.getcwd()

from PyInstaller.utils.hooks import collect_data_files

# include necessary data files
datas = collect_data_files("osxphotos")
datas.extend(
    [
        ("osxphotos/templates/xmp_sidecar.mako", "osxphotos/templates"),
        ("osxphotos/templates/xmp_sidecar_beta.mako", "osxphotos/templates"),
        ("osxphotos/phototemplate.tx", "osxphotos"),
        ("osxphotos/phototemplate.md", "osxphotos"),
        ("osxphotos/tutorial.md", "osxphotos"),
        ("osxphotos/exiftool_filetypes.json", "osxphotos"),
        ("osxphotos/docs", "osxphotos/docs"),
    ]
)

package_imports = [
    ["photoscript", ["photoscript.applescript"]],
    ["utitools", ["uti.csv", "uti_tree.json"]],
]
for package, files in package_imports:
    proot = os.path.dirname(importlib.import_module(package).__file__)
    datas.extend((os.path.join(proot, f), package) for f in files)

# Add attribute data files for osxmetadata
# There is probably a better way to do this but this works
proot = os.path.dirname(importlib.import_module("osxmetadata").__file__)
for attribute_data in [
    "audio_attributes.json",
    "common_attributes.json",
    "filesystem_attributes.json",
    "image_attributes.json",
    "mdimporter_constants.json",
    "nsurl_resource_keys.json",
    "video_attributes.json",
]:
    datas.append(
        (
            os.path.join(proot, "attribute_data", attribute_data),
            "osxmetadata/attribute_data",
        )
    )

block_cipher = None

a = Analysis(
    ["cli.py"],
    pathex=[pathex],
    binaries=[
        ("osxphotos/lib/libdisclaim.dylib", "osxphotos/lib"),
        ("osxphotos/lib/libdisclaim_x86_64.dylib", "osxphotos/lib"),
        ("osxphotos/lib/libdisclaim_arm64.dylib", "osxphotos/lib"),
    ],
    datas=datas,
    hiddenimports=[
        "pkg_resources.py2_warn",
        # Lazy-loaded CLI commands (needed for LazyGroup)
        "osxphotos.cli.about",
        "osxphotos.cli.albums",
        "osxphotos.cli.compare",
        "osxphotos.cli.debug_dump",
        "osxphotos.cli.docs",
        "osxphotos.cli.dump",
        "osxphotos.cli.exiftool_cli",
        "osxphotos.cli.export",
        "osxphotos.cli.exportdb",
        "osxphotos.cli.grep",
        "osxphotos.cli.help",
        "osxphotos.cli.info",
        "osxphotos.cli.install_uninstall_run",
        "osxphotos.cli.keywords",
        "osxphotos.cli.labels",
        "osxphotos.cli.list",
        "osxphotos.cli.orphans",
        "osxphotos.cli.persons",
        "osxphotos.cli.places",
        "osxphotos.cli.query",
        "osxphotos.cli.repl",
        "osxphotos.cli.snap_diff",
        "osxphotos.cli.template_repl",
        "osxphotos.cli.theme",
        "osxphotos.cli.tutorial",
        "osxphotos.cli.update_command",
        "osxphotos.cli.version",
        # macOS-specific commands
        "osxphotos.cli.add_locations",
        "osxphotos.cli.batch_edit",
        "osxphotos.cli.import_cli",
        "osxphotos.cli.photo_inspect",
        "osxphotos.cli.push_exif",
        "osxphotos.cli.show_command",
        "osxphotos.cli.sync",
        "osxphotos.cli.timewarp",
        "osxphotos.cli.uuid",
        # Lazy-loaded main package modules
        "osxphotos.albuminfo",
        "osxphotos.exifinfo",
        "osxphotos.exiftool",
        "osxphotos.exifwriter",
        "osxphotos.export_db",
        "osxphotos.exportoptions",
        "osxphotos.fileutil",
        "osxphotos.iphoto",
        "osxphotos.momentinfo",
        "osxphotos.personinfo",
        "osxphotos.photoexporter",
        "osxphotos.photoinfo",
        "osxphotos.photoquery",
        "osxphotos.photosdb",
        "osxphotos.photosdb._photosdb_process_comments",
        "osxphotos.phototables",
        "osxphotos.phototemplate",
        "osxphotos.placeinfo",
        "osxphotos.scoreinfo",
        "osxphotos.searchinfo",
        "osxphotos.sidecars",
        "osxphotos.photosalbum",
    ],
    hookspath=[],
    # runtime_hooks=["disclaim.py"],
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
    name="osxphotos",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    target_architecture="universal2",
)
