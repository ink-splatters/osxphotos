#!/bin/bash
# Build universal2 (arm64 + x86_64) libdisclaim dylib

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LIB_DIR="$PROJECT_ROOT/osxphotos/lib"

echo "Building universal2 libdisclaim..."
echo "Project root: $PROJECT_ROOT"
echo "Library directory: $LIB_DIR"

# Create lib directory if it doesn't exist
mkdir -p "$LIB_DIR"

# Clean up old builds
rm -f "$LIB_DIR/libdisclaim_arm64.dylib" \
      "$LIB_DIR/libdisclaim_x86_64.dylib" \
      "$LIB_DIR/libdisclaim.dylib" \
      "/tmp/libdisclaim_arm64.dylib" \
      "/tmp/libdisclaim_x86_64.dylib"

# Build for arm64
echo "Building arm64 slice..."
clang++ -arch arm64 -dynamiclib -std=c++11 -O3 \
    -framework CoreFoundation \
    -o "/tmp/libdisclaim_arm64.dylib" \
    "$PROJECT_ROOT/disclaim.cpp"

# Build for x86_64
echo "Building x86_64 slice..."
clang++ -arch x86_64 -dynamiclib -std=c++11 -O3 \
    -framework CoreFoundation \
    -o "/tmp/libdisclaim_x86_64.dylib" \
    "$PROJECT_ROOT/disclaim.cpp"

# Create universal2 binary using lipo
echo "Creating universal2 binary..."
lipo -create \
    "/tmp/libdisclaim_arm64.dylib" \
    "/tmp/libdisclaim_x86_64.dylib" \
    -output "$LIB_DIR/libdisclaim.dylib"

# Also keep separate arch libraries for backward compatibility
cp "/tmp/libdisclaim_arm64.dylib" "$LIB_DIR/libdisclaim_arm64.dylib"
cp "/tmp/libdisclaim_x86_64.dylib" "$LIB_DIR/libdisclaim_x86_64.dylib"

# Clean up temp files
rm -f "/tmp/libdisclaim_arm64.dylib" "/tmp/libdisclaim_x86_64.dylib"

# Verify the universal binary
echo ""
echo "Verifying universal2 binary:"
file "$LIB_DIR/libdisclaim.dylib"
lipo -info "$LIB_DIR/libdisclaim.dylib"

echo ""
echo "Build complete!"
echo "  Universal2: $LIB_DIR/libdisclaim.dylib"
echo "  arm64:      $LIB_DIR/libdisclaim_arm64.dylib"
echo "  x86_64:     $LIB_DIR/libdisclaim_x86_64.dylib"

