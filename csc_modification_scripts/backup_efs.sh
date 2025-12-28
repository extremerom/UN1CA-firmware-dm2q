#!/system/bin/sh
# CSC Backup Script
# CRITICAL: Run this before making any CSC modifications!

set -e

BACKUP_DIR="/sdcard/CSC_Backup_$(date +%Y%m%d_%H%M%S)"

echo "======================================"
echo "CSC and EFS Backup Script"
echo "======================================"
echo ""
echo "Backup location: $BACKUP_DIR"
echo ""

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: This script must be run as root!"
    echo "Use: su -c 'sh backup_efs.sh'"
    exit 1
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo "Step 1: Backing up system properties..."
getprop > "$BACKUP_DIR/all_properties.txt"
getprop | grep -i csc > "$BACKUP_DIR/csc_properties.txt"
getprop | grep sales > "$BACKUP_DIR/sales_properties.txt"
echo "✓ Properties backed up"

echo ""
echo "Step 2: Backing up EFS partition..."
# Full EFS partition backup
if [ -e /dev/block/by-name/efs ]; then
    dd if=/dev/block/by-name/efs of="$BACKUP_DIR/efs_partition.img" bs=4096
    echo "✓ EFS partition backed up to efs_partition.img"
else
    echo "! Warning: EFS partition not found at /dev/block/by-name/efs"
fi

# Backup EFS directory contents
echo ""
echo "Step 3: Backing up EFS directory contents..."
if [ -d /efs ]; then
    tar -czf "$BACKUP_DIR/efs_contents.tar.gz" /efs 2>/dev/null || echo "! Some EFS files may have been skipped"
    echo "✓ EFS contents backed up to efs_contents.tar.gz"
    
    # Backup important EFS files individually
    if [ -f /efs/imei/mps_code.dat ]; then
        cp /efs/imei/mps_code.dat "$BACKUP_DIR/" 2>/dev/null
        cat /efs/imei/mps_code.dat > "$BACKUP_DIR/mps_code_readable.txt"
        echo "✓ MPS code: $(cat /efs/imei/mps_code.dat)"
    fi
    
    if [ -f /efs/imei/sales_code.dat ]; then
        cp /efs/imei/sales_code.dat "$BACKUP_DIR/" 2>/dev/null
        cat /efs/imei/sales_code.dat > "$BACKUP_DIR/sales_code_readable.txt"
        echo "✓ Sales code: $(cat /efs/imei/sales_code.dat)"
    fi
else
    echo "! Warning: /efs directory not found"
fi

echo ""
echo "Step 4: Backing up build.prop files..."
for prop_file in /system/build.prop /vendor/build.prop /product/etc/build.prop; do
    if [ -f "$prop_file" ]; then
        cp "$prop_file" "$BACKUP_DIR/$(basename $(dirname $prop_file))_build.prop" 2>/dev/null || true
        echo "✓ Backed up $prop_file"
    fi
done

echo ""
echo "Step 5: Backing up CSC data..."
if [ -d /data/csc ]; then
    tar -czf "$BACKUP_DIR/csc_data.tar.gz" /data/csc 2>/dev/null || echo "! Some CSC data files may have been skipped"
    echo "✓ CSC data backed up"
fi

echo ""
echo "Step 6: Creating backup summary..."
cat > "$BACKUP_DIR/backup_info.txt" << EOF
CSC/EFS Backup Information
==========================
Date: $(date)
Device: $(getprop ro.product.model)
Android Version: $(getprop ro.build.version.release)
Build: $(getprop ro.build.display.id)

Current CSC Information:
- ro.csc.sales_code: $(getprop ro.csc.sales_code)
- ril.sales_code: $(getprop ril.sales_code)
- persist.sys.csc_code: $(getprop persist.sys.csc_code)
- ro.product.name: $(getprop ro.product.name)

EFS Files:
- MPS Code: $(cat /efs/imei/mps_code.dat 2>/dev/null || echo "Not found")
- Sales Code: $(cat /efs/imei/sales_code.dat 2>/dev/null || echo "Not found")

Backup Contents:
$(ls -lh "$BACKUP_DIR")
EOF

echo "✓ Backup summary created"

echo ""
echo "======================================"
echo "Backup Complete!"
echo "======================================"
echo ""
echo "Backup location: $BACKUP_DIR"
echo ""
echo "IMPORTANT:"
echo "1. Copy this backup to your computer"
echo "2. Keep multiple copies in safe locations"
echo "3. This backup is critical for recovery"
echo ""
echo "To copy to computer via ADB:"
echo "  adb pull $BACKUP_DIR"
echo ""
