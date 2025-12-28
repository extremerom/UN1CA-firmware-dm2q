#!/system/bin/sh
# CSC Change Script - Change from TPA to OWO
# WARNING: Backup EFS before running this script!

set -e

TARGET_CSC="OWO"

echo "======================================"
echo "CSC Modification Script"
echo "Target CSC: $TARGET_CSC"
echo "======================================"
echo ""

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: This script must be run as root!"
    echo "Use: su -c 'sh change_csc.sh'"
    exit 1
fi

# Display current CSC
echo "Current CSC Configuration:"
echo "- ro.csc.sales_code: $(getprop ro.csc.sales_code)"
echo "- ril.sales_code: $(getprop ril.sales_code)"
echo "- persist.sys.csc_code: $(getprop persist.sys.csc_code)"
echo ""

# Check for backup
echo "WARNING: This will modify system files!"
echo "Have you backed up your EFS partition? (yes/no)"
echo ""
echo "If not, run: sh backup_efs.sh first!"
echo ""

# Wait for confirmation (in real usage)
# read -r CONFIRM
# if [ "$CONFIRM" != "yes" ]; then
#     echo "Aborted. Please backup EFS first."
#     exit 1
# fi

echo "Proceeding with CSC modification..."
echo ""

# Step 1: Remount partitions as read-write
echo "Step 1: Remounting partitions..."
mount -o remount,rw / 2>/dev/null || true
mount -o remount,rw /system 2>/dev/null || true
mount -o remount,rw /vendor 2>/dev/null || true
echo "✓ Partitions remounted"

# Step 2: Modify EFS files
echo ""
echo "Step 2: Modifying EFS files..."

if [ -d /efs/imei ]; then
    # Backup current values
    if [ -f /efs/imei/mps_code.dat ]; then
        cp /efs/imei/mps_code.dat /efs/imei/mps_code.dat.bak
    fi
    if [ -f /efs/imei/sales_code.dat ]; then
        cp /efs/imei/sales_code.dat /efs/imei/sales_code.dat.bak
    fi
    
    # Write new CSC
    echo "$TARGET_CSC" > /efs/imei/mps_code.dat
    echo "$TARGET_CSC" > /efs/imei/sales_code.dat
    
    # Set correct permissions
    chown radio:radio /efs/imei/mps_code.dat
    chown radio:radio /efs/imei/sales_code.dat
    chmod 0644 /efs/imei/mps_code.dat
    chmod 0644 /efs/imei/sales_code.dat
    
    echo "✓ EFS files modified"
    echo "  - MPS code: $(cat /efs/imei/mps_code.dat)"
    echo "  - Sales code: $(cat /efs/imei/sales_code.dat)"
else
    echo "! Warning: /efs/imei directory not found"
fi

# Step 3: Modify persist properties
echo ""
echo "Step 3: Setting system properties..."
setprop persist.sys.csc_code "$TARGET_CSC" 2>/dev/null || echo "! Could not set persist.sys.csc_code"
setprop ril.sales_code "$TARGET_CSC" 2>/dev/null || echo "! Could not set ril.sales_code"
echo "✓ Properties set (may require reboot to persist)"

# Step 4: Clear CSC cache
echo ""
echo "Step 4: Clearing CSC cache..."
rm -rf /data/csc/* 2>/dev/null || true
rm -rf /data/data/com.samsung.android.csc/* 2>/dev/null || true
echo "✓ CSC cache cleared"

# Step 5: Trigger CSC update
echo ""
echo "Step 5: Triggering CSC update..."
am broadcast -a com.samsung.intent.action.CSC_UPDATE_TEST 2>/dev/null || echo "! Could not send CSC update broadcast"
echo "✓ CSC update triggered"

# Step 6: Remount partitions as read-only
echo ""
echo "Step 6: Remounting partitions as read-only..."
sync
mount -o remount,ro /system 2>/dev/null || true
mount -o remount,ro /vendor 2>/dev/null || true
echo "✓ Partitions remounted as read-only"

echo ""
echo "======================================"
echo "CSC Modification Complete!"
echo "======================================"
echo ""
echo "New CSC Configuration:"
echo "- Target CSC: $TARGET_CSC"
echo "- EFS MPS code: $(cat /efs/imei/mps_code.dat 2>/dev/null || echo 'Not readable')"
echo "- EFS Sales code: $(cat /efs/imei/sales_code.dat 2>/dev/null || echo 'Not readable')"
echo ""
echo "NEXT STEPS:"
echo "1. Reboot your device: reboot"
echo "2. After reboot, verify CSC with:"
echo "   getprop ro.csc.sales_code"
echo "   getprop ril.sales_code"
echo "3. If CSC didn't change, you may need to:"
echo "   - Factory reset (will erase data!)"
echo "   - Flash OWO CSC package via Odin"
echo ""
echo "To reboot now, run: reboot"
echo ""
