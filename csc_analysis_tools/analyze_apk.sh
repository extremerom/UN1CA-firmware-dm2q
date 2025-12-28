#!/bin/bash
# CSC APK Analysis Script
# Analyzes APK files for CSC-related strings and configurations

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="/tmp/apk_analysis"

echo "==================================="
echo "CSC APK Analysis Tool"
echo "==================================="

# Create working directory
mkdir -p "$WORK_DIR"

# Function to analyze an APK
analyze_apk() {
    local apk_path="$1"
    local apk_name=$(basename "$apk_path")
    local output_dir="$WORK_DIR/${apk_name%.apk}"
    
    echo ""
    echo "Analyzing: $apk_name"
    echo "-----------------------------------"
    
    # Decompile APK
    if [ -d "$output_dir" ]; then
        rm -rf "$output_dir"
    fi
    
    apktool d "$apk_path" -o "$output_dir" -f 2>/dev/null || {
        echo "ERROR: Failed to decompile $apk_name"
        return 1
    }
    
    # Search for CSC-related strings
    echo "Searching for CSC-related strings..."
    grep -r "ro.csc\|sales_code\|CSC\|TPA\|OWO" "$output_dir" --include="*.smali" --include="*.xml" 2>/dev/null | head -20 || echo "No CSC strings found"
    
    # Look for property access
    echo ""
    echo "Property access patterns:"
    grep -r "SystemProperties\|getprop\|setprop" "$output_dir" --include="*.smali" 2>/dev/null | grep -i "csc\|sales" | head -10 || echo "No property access found"
    
    echo ""
}

# Analyze CSC.apk
CSC_APK="$SCRIPT_DIR/../system/system/priv-app/CSC/CSC.apk"
if [ -f "$CSC_APK" ]; then
    analyze_apk "$CSC_APK"
else
    echo "ERROR: CSC.apk not found at $CSC_APK"
fi

echo ""
echo "==================================="
echo "Analysis complete. Results in: $WORK_DIR"
echo "==================================="
