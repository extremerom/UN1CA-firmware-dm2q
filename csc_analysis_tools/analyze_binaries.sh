#!/bin/bash
# Binary and Library Analysis Script
# Uses readelf and strings to analyze .so and binary files for CSC references

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIRMWARE_DIR="$SCRIPT_DIR/.."

echo "==================================="
echo "Binary and Library Analysis Tool"
echo "==================================="

# Function to analyze a binary/library
analyze_binary() {
    local file_path="$1"
    local file_name=$(basename "$file_path")
    
    echo ""
    echo "Analyzing: $file_name"
    echo "-----------------------------------"
    
    # Check if it's an ELF file
    if file "$file_path" | grep -q "ELF"; then
        echo "ELF Information:"
        readelf -h "$file_path" 2>/dev/null | grep -E "Machine|Class|Type" || true
        
        echo ""
        echo "Dynamic dependencies:"
        readelf -d "$file_path" 2>/dev/null | grep NEEDED | head -10 || echo "No dependencies found"
        
        echo ""
        echo "CSC-related strings:"
        strings "$file_path" | grep -i "csc\|sales_code\|TPA\|OWO" || echo "No CSC strings found"
        
        echo ""
        echo "Property-related strings:"
        strings "$file_path" | grep -E "ro\.|persist\.|efs" | grep -i "csc\|sales" || echo "No property strings found"
    else
        echo "Not an ELF file, performing basic string analysis..."
        strings "$file_path" | grep -i "csc\|sales_code" | head -10 || echo "No CSC strings found"
    fi
    
    echo ""
}

echo ""
echo "Searching for binaries with CSC references..."
echo "-----------------------------------"

# Search vendor binaries
if [ -d "$FIRMWARE_DIR/vendor/bin" ]; then
    echo "Scanning vendor binaries..."
    for binary in "$FIRMWARE_DIR/vendor/bin"/*; do
        if [ -f "$binary" ] && strings "$binary" 2>/dev/null | grep -q "sales_code"; then
            analyze_binary "$binary"
        fi
    done
fi

# Search system binaries
if [ -d "$FIRMWARE_DIR/system/system/bin" ]; then
    echo "Scanning system binaries..."
    for binary in "$FIRMWARE_DIR/system/system/bin"/*; do
        if [ -f "$binary" ] && strings "$binary" 2>/dev/null | grep -q "sales_code"; then
            analyze_binary "$binary"
        fi
    done
fi

# Search vendor libraries
echo ""
echo "Searching vendor libraries..."
find "$FIRMWARE_DIR/vendor/lib" "$FIRMWARE_DIR/vendor/lib64" -name "*.so" 2>/dev/null | while read -r lib; do
    if strings "$lib" 2>/dev/null | grep -q "sales_code"; then
        echo "Found CSC reference in: $(basename "$lib")"
        strings "$lib" | grep -i "csc\|sales_code" | head -5
    fi
done

echo ""
echo "==================================="
echo "Binary analysis complete"
echo "==================================="
