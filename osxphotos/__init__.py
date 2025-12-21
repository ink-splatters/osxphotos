"""__init__.py for osxphotos"""

from __future__ import annotations

import logging

# Import only lightweight, essential items eagerly
from ._constants import AlbumSortOrder
from ._version import __version__
from .debug import is_debug, set_debug
from .platform import is_macos

# Configure logging; every module in osxphotos should use this logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
)
logger: logging.Logger = logging.getLogger("osxphotos")
if not is_debug():
    logging.disable(logging.DEBUG)

__all__ = [
    "AlbumInfo",
    "AlbumSortOrder",
    "CommentInfo",
    "ExifInfo",
    "ExifTool",
    "ExifWriter",
    "ExportDB",
    "ExportDBTemp",
    "ExportOptions",
    "ExportResults",
    "FaceInfo",
    "FileUtil",
    "FileUtilNoOp",
    "FolderInfo",
    "ImportInfo",
    "LikeInfo",
    "MomentInfo",
    "PersonInfo",
    "PhotoExporter",
    "PhotoInfo",
    "PhotoTables",
    "PhotoTemplate",
    "PhotosAlbum",
    "PhotosAlbumPhotoScript",
    "PhotosDB",
    "PlaceInfo",
    "ProjectInfo",
    "QueryOptions",
    "ScoreInfo",
    "SearchInfo",
    "SidecarWriter",
    "__version__",
    "iPhotoAlbumInfo",
    "iPhotoDB",
    "iPhotoFaceInfo",
    "iPhotoFolderInfo",
    "iPhotoPersonInfo",
    "iPhotoPhotoInfo",
    "is_debug",
    "logger",
    "set_debug",
]

# Lazy loading mapping for heavy imports
_LAZY_IMPORTS = {
    "AlbumInfo": ("osxphotos.albuminfo", "AlbumInfo"),
    "FolderInfo": ("osxphotos.albuminfo", "FolderInfo"),
    "ImportInfo": ("osxphotos.albuminfo", "ImportInfo"),
    "ProjectInfo": ("osxphotos.albuminfo", "ProjectInfo"),
    "ExifInfo": ("osxphotos.exifinfo", "ExifInfo"),
    "ExifTool": ("osxphotos.exiftool", "ExifTool"),
    "ExifWriter": ("osxphotos.exifwriter", "ExifWriter"),
    "ExportDB": ("osxphotos.export_db", "ExportDB"),
    "ExportDBTemp": ("osxphotos.export_db", "ExportDBTemp"),
    "ExportOptions": ("osxphotos.exportoptions", "ExportOptions"),
    "ExportResults": ("osxphotos.exportoptions", "ExportResults"),
    "FileUtil": ("osxphotos.fileutil", "FileUtil"),
    "FileUtilNoOp": ("osxphotos.fileutil", "FileUtilNoOp"),
    "iPhotoAlbumInfo": ("osxphotos.iphoto", "iPhotoAlbumInfo"),
    "iPhotoDB": ("osxphotos.iphoto", "iPhotoDB"),
    "iPhotoFaceInfo": ("osxphotos.iphoto", "iPhotoFaceInfo"),
    "iPhotoFolderInfo": ("osxphotos.iphoto", "iPhotoFolderInfo"),
    "iPhotoPersonInfo": ("osxphotos.iphoto", "iPhotoPersonInfo"),
    "iPhotoPhotoInfo": ("osxphotos.iphoto", "iPhotoPhotoInfo"),
    "MomentInfo": ("osxphotos.momentinfo", "MomentInfo"),
    "FaceInfo": ("osxphotos.personinfo", "FaceInfo"),
    "PersonInfo": ("osxphotos.personinfo", "PersonInfo"),
    "PhotoExporter": ("osxphotos.photoexporter", "PhotoExporter"),
    "PhotoInfo": ("osxphotos.photoinfo", "PhotoInfo"),
    "QueryOptions": ("osxphotos.photoquery", "QueryOptions"),
    "PhotosDB": ("osxphotos.photosdb", "PhotosDB"),
    "CommentInfo": ("osxphotos.photosdb._photosdb_process_comments", "CommentInfo"),
    "LikeInfo": ("osxphotos.photosdb._photosdb_process_comments", "LikeInfo"),
    "PhotoTables": ("osxphotos.phototables", "PhotoTables"),
    "PhotoTemplate": ("osxphotos.phototemplate", "PhotoTemplate"),
    "PlaceInfo": ("osxphotos.placeinfo", "PlaceInfo"),
    "ScoreInfo": ("osxphotos.scoreinfo", "ScoreInfo"),
    "SearchInfo": ("osxphotos.searchinfo", "SearchInfo"),
    "SidecarWriter": ("osxphotos.sidecars", "SidecarWriter"),
}

# Add macOS-specific imports
if is_macos:
    _LAZY_IMPORTS.update({
        "PhotosAlbum": ("osxphotos.photosalbum", "PhotosAlbum"),
        "PhotosAlbumPhotoScript": ("osxphotos.photosalbum", "PhotosAlbumPhotoScript"),
    })

# Cache for lazy-loaded modules
_lazy_cache = {}


def __getattr__(name: str):
    """Lazy load heavy modules on first access."""
    if name in _lazy_cache:
        return _lazy_cache[name]
    
    if name in _LAZY_IMPORTS:
        module_name, attr_name = _LAZY_IMPORTS[name]
        try:
            import importlib
            module = importlib.import_module(module_name)
            attr = getattr(module, attr_name)
            _lazy_cache[name] = attr
            return attr
        except (ImportError, AttributeError) as e:
            raise AttributeError(
                f"Module {__name__!r} has no attribute {name!r}"
            ) from e
    
    raise AttributeError(f"Module {__name__!r} has no attribute {name!r}")


def __dir__():
    """Include lazy-loaded attributes in dir()."""
    return sorted(__all__)
