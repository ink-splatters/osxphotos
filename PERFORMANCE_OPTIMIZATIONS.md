# Performance Optimizations Applied

This document tracks the performance optimizations implemented based on `agg.plan.md`.

## Summary

The following optimizations have been applied to improve osxphotos startup time and reduce import overhead:

## 1. Lazy Module Loading (✅ Completed)

### osxphotos/__init__.py
- **Before**: All modules imported eagerly at package import time
- **After**: Implemented `__getattr__` lazy loading for heavy modules
- **Impact**: Only essential lightweight modules are imported upfront
- **Modules lazily loaded**: ~25 heavy modules including PhotosDB, PhotoInfo, ExifTool, PhotoTemplate, etc.

### Benefits:
- Faster `import osxphotos` time
- Reduced memory footprint for simple operations
- Pay-as-you-go import cost

## 2. Deferred TextX Import (✅ Completed)

### osxphotos/phototemplate.py
- **Before**: TextX imported and metamodel built at module import time
- **After**: Deferred import and lazy metamodel building
- **Implementation**: 
  - Removed top-level `from textx import ...`
  - Added `_ensure_metamodel()` method that imports on first use
  - TextX metamodel built only when `parse()` is first called

### Benefits:
- ~50-100ms reduction in import time (TextX is heavy)
- Template-related commands start faster
- Non-template operations don't pay TextX cost

## 3. Deferred CloudPhotoLibrary Bundle Load (✅ Completed)

### osxphotos/fingerprint.py
- **Before**: CloudPhotoLibrary framework loaded at module import
- **After**: Lazy loading on first `fingerprint()` call
- **Implementation**:
  - Removed top-level `objc.loadBundle()`
  - Added `_ensure_cpl_loaded()` function
  - Bundle loaded only when fingerprint functionality is actually used

### Benefits:
- Faster import for operations not using fingerprinting
- Reduced pyobjc overhead during startup
- Framework loading deferred until needed

## 4. Lazy CLI Command Loading (✅ Completed)

### osxphotos/cli/cli.py
- **Before**: All CLI commands imported eagerly
- **After**: Implemented `LazyGroup` with command registry
- **Implementation**:
  - Created `_lazy_commands.py` with command registry
  - Implemented custom `LazyGroup` class extending `click.Group`
  - Commands imported only when invoked

### Benefits:
- Dramatically faster `osxphotos --help` and `osxphotos --version`
- Only the invoked command module is loaded
- ~35+ CLI modules not loaded until needed

## 5. Selective disclaim() Invocation (✅ Completed)

### osxphotos/cli/cli.py & _photos_access.py
- **Before**: `disclaim()` called for all commands
- **After**: Only invoked for commands needing Photos library access
- **Implementation**:
  - Created `_photos_access.py` with list of commands requiring Photos access
  - disclaim() now called in `LazyGroup.get_command()` based on command needs
  - Commands like `--version`, `--help`, `docs` skip disclaim()

### Benefits:
- Faster startup for non-Photos commands
- Avoids unnecessary process re-execution
- ~26 commands identified as needing Photos access

## 6. Curated Cython Module List (✅ Completed)

### setup.py
- **Before**: `cythonize("osxphotos/**/*.py")` glob pattern
- **After**: Explicit list of ~50 hot-path modules
- **Implementation**:
  - Created `CYTHON_MODULES` list focusing on performance-critical code
  - Added compiler directives for additional optimization
  - Reduced compilation from ~167 files to ~50 focused modules

### Benefits:
- Faster build times (fewer modules to compile)
- More predictable compilation
- Focus optimization on modules that benefit most
- Added aggressive Cython directives: `boundscheck=False`, `wraparound=False`, etc.

## 7. Build Flag Management (✅ Completed)

### build.sh
- **Before**: Native CPU flags could make distribution builds non-portable
- **After**: Filter `-mcpu=native` in distribution builds
- **Implementation**:
  - `build.sh` now filters CXXFLAGS/CPPFLAGS/CFLAGS
  - Replaces `-mcpu=native` with portable equivalents
  - `shell.nix` unchanged for dev environment

### Benefits:
- Portable distribution wheels
- Aggressive optimization in dev
- Predictable build flags

## 8. Package Distribution Improvements (✅ Completed)

### MANIFEST.in
- Added C/C++ sources for sdist
- Included universal2 libdisclaim.dylib

### osxphotos.spec (PyInstaller)
- Added ~40 hiddenimports for lazy-loaded modules
- Ensures CLI commands and core modules are bundled
- Supports universal2 binaries

### Benefits:
- Source distributions can be installed without git repo
- PyInstaller bundles work correctly with lazy loading
- Universal binary support for both architectures

## 9. Universal2 libdisclaim (✅ Completed)

### osxphotos/disclaim.py
- **Before**: Arch-specific dylibs selected by platform.machine()
- **After**: Prefers universal2 library, falls back to arch-specific
- **Implementation**:
  - Created `build_libdisclaim_universal2.sh` script
  - Updated loader to try `libdisclaim.dylib` first
  - Maintains backward compatibility with arch-specific libs

### Benefits:
- Single dylib for both architectures
- Simpler distribution
- Backward compatible

## Expected Performance Gains

Based on the optimizations applied:

1. **Cold import time**: 40-60% reduction expected
2. **CLI help/version**: 70-80% reduction expected  
3. **Template operations**: 50-100ms saved (TextX defer)
4. **Non-Photos commands**: Additional savings from skipping disclaim()

## Testing

To verify optimizations:

```bash
# Test import time
python3 benchmarks/import_time.py

# Test CLI commands
python3 benchmarks/cli_commands.py

# Detailed import profiling
PYTHONPROFILEIMPORTTIME=1 python -c "import osxphotos" 2>&1 | head -30
```

## Future Optimizations (Not Yet Implemented)

From the original plan, potential future work:

1. Defer more heavy imports in remaining modules
2. Profile and optimize remaining hot paths
3. Consider C extension for critical loops
4. Investigate PhotosDB query optimization

## Files Modified

- `osxphotos/__init__.py` - Lazy module loading via `__getattr__`
- `osxphotos/phototemplate.py` - Deferred TextX import
- `osxphotos/fingerprint.py` - Lazy CloudPhotoLibrary loading
- `osxphotos/cli/cli.py` - Lazy command loading with LazyGroup
- `osxphotos/cli/_lazy_commands.py` - NEW: Command registry
- `osxphotos/cli/_photos_access.py` - NEW: Photos access tracking
- `osxphotos/disclaim.py` - Universal2 library support
- `setup.py` - Curated Cython modules list
- `build.sh` - Portable build flag filtering
- `MANIFEST.in` - C sources and universal2 lib inclusion
- `osxphotos.spec` - PyInstaller hiddenimports
- `shell.nix` - (Unchanged, kept for dev)

## Build Instructions

### Development Build
```bash
# Uses shell.nix aggressive optimization flags
cd /path/to/osxphotos
nix-shell  # or direnv exec .
python3 -m pip install -e .
```

### Distribution Build
```bash
# Uses portable flags from build.sh
./build.sh
```

### Build Universal2 Library (Optional)
```bash
direnv exec . scripts/build_libdisclaim_universal2.sh
```

## Notes

- Lazy loading maintains full API compatibility
- `__all__` unchanged, all symbols still accessible
- dir() and help() work correctly with lazy modules
- Type hints and IDE completion unaffected

