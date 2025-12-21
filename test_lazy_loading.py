#!/usr/bin/env python3
"""Quick test to verify lazy loading is working."""

import sys
import time

print("Testing lazy loading optimizations...")
print("=" * 60)

# Test 1: Basic import
print("\n1. Testing basic import osxphotos...")
start = time.perf_counter()
import osxphotos
end = time.perf_counter()
print(f"   ✓ Import successful: {end - start:.4f}s")

# Test 2: Check __version__ is available
print("\n2. Testing __version__ (should be fast)...")
start = time.perf_counter()
version = osxphotos.__version__
end = time.perf_counter()
print(f"   ✓ Version {version}: {end - start:.6f}s")

# Test 3: Check that heavy modules are NOT loaded yet
print("\n3. Verifying lazy modules not loaded yet...")
loaded_heavy = []
for name in ['PhotosDB', 'PhotoTemplate', 'ExifTool', 'PhotoInfo']:
    if name in osxphotos._lazy_cache:
        loaded_heavy.append(name)

if not loaded_heavy:
    print(f"   ✓ No heavy modules loaded yet (correct)")
else:
    print(f"   ⚠ Some modules already loaded: {loaded_heavy}")

# Test 4: Access a lazy-loaded module
print("\n4. Testing lazy load of PhotosDB...")
start = time.perf_counter()
PhotosDB = osxphotos.PhotosDB
end = time.perf_counter()
print(f"   ✓ PhotosDB loaded on demand: {end - start:.4f}s")

# Test 5: Verify it's cached now
print("\n5. Verifying caching works...")
if 'PhotosDB' in osxphotos._lazy_cache:
    print(f"   ✓ PhotosDB now in cache")
else:
    print(f"   ⚠ PhotosDB not cached (unexpected)")

# Test 6: Second access should be instant
start = time.perf_counter()
PhotosDB2 = osxphotos.PhotosDB
end = time.perf_counter()
print(f"   ✓ Cached access: {end - start:.6f}s (should be < 0.001s)")

# Test 7: Check dir() works
print("\n6. Testing dir() includes lazy modules...")
all_attrs = dir(osxphotos)
expected = ['PhotosDB', 'PhotoInfo', 'ExifTool', 'PhotoTemplate']
found = [name for name in expected if name in all_attrs]
if len(found) == len(expected):
    print(f"   ✓ All expected symbols in dir(): {len(found)}/{len(expected)}")
else:
    print(f"   ⚠ Missing symbols: {set(expected) - set(found)}")

print("\n" + "=" * 60)
print("Lazy loading test complete!")

