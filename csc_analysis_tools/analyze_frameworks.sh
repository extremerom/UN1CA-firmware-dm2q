#!/bin/bash
# Framework and JAR Analysis Script
# Analyzes framework JARs for CSC-related code

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIRMWARE_DIR="$SCRIPT_DIR/.."
WORK_DIR="/tmp/jar_analysis"

echo "==================================="
echo "Framework/JAR Analysis Tool"
echo "==================================="

mkdir -p "$WORK_DIR"

# Function to analyze a JAR file
analyze_jar() {
    local jar_path="$1"
    local jar_name=$(basename "$jar_path")
    local extract_dir="$WORK_DIR/${jar_name%.jar}"
    
    echo ""
    echo "Analyzing: $jar_name"
    echo "-----------------------------------"
    
    # Extract JAR
    mkdir -p "$extract_dir"
    unzip -q "$jar_path" -d "$extract_dir" 2>/dev/null || {
        echo "ERROR: Failed to extract $jar_name"
        return 1
    }
    
    # Search for CSC-related content
    echo "Searching for CSC-related strings..."
    find "$extract_dir" -type f \( -name "*.class" -o -name "*.dex" \) -exec strings {} \; 2>/dev/null | \
        grep -i "sales_code\|ro.csc\|CSC" | head -10 || echo "No CSC strings found"
    
    # List classes
    echo ""
    echo "Classes in JAR:"
    find "$extract_dir" -name "*.class" | head -10 | sed 's|.*/||'
    
    echo ""
}

# Search for framework JARs
echo ""
echo "Searching framework JARs..."
if [ -d "$FIRMWARE_DIR/system_ext/framework" ]; then
    find "$FIRMWARE_DIR/system_ext/framework" -name "*.jar" | head -5 | while read -r jar; do
        if strings "$jar" 2>/dev/null | grep -q -i "csc\|sales"; then
            analyze_jar "$jar"
        fi
    done
fi

echo ""
echo "==================================="
echo "Framework analysis complete"
echo "==================================="
