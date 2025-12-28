# CSC Modification Guide - Samsung SM-S916B (dm2q)

## Overview
This guide provides methods to permanently change the CSC (Country-Specific Code) from TPA to OWO on Samsung Galaxy S23+ (SM-S916B).

**Current CSC**: SAOMC_SM-S916B_OWO_TPA_16_0009 TPA/TPA,TPA/TPA  
**Target CSC**: OWO

## Prerequisites
- Root access (required)
- ADB enabled
- Backup of EFS partition (CRITICAL!)

## Understanding CSC
CSC (Country-Specific Code) controls:
- Carrier-specific features
- Regional settings
- Pre-installed apps
- Network configurations
- VoLTE/VoWiFi settings

CSC information is stored in multiple locations:
1. System properties (`ro.csc.sales_code`, `ril.sales_code`, `persist.sys.csc_code`)
2. EFS partition (`/efs/imei/mps_code.dat`, `/efs/imei/sales_code.dat`)
3. Persist partition (`/persist/csc_code`)
4. Build properties in system partitions

## Analysis Results

### Key Files and Locations

#### 1. CSC APK
- **Location**: `/system/priv-app/CSC/CSC.apk`
- **Purpose**: Handles CSC updates and configurations
- **Key Classes**: 
  - CSC Ringtone Manager (reads `ro.csc.sales_code`)
  - CSC Compare Service (monitors CSC changes)
  - CSC Update Service

#### 2. System Properties
Key properties that control CSC:
```
ro.csc.sales_code         # Read-only CSC code
ril.sales_code            # RIL sales code
persist.sys.csc_code      # Persistent CSC code
ro.csc.country_code       # Country code
ro.csc.countryiso_code    # ISO country code
```

#### 3. EFS Partition Files
The EFS (Encrypted File System) partition stores persistent device data:
```
/efs/imei/mps_code.dat        # Multi-CSC sales code
/efs/imei/sales_code.dat      # Sales code
/efs/imei/sms_list.dat        # SMS configuration
```

#### 4. Vendor Binaries
Binary with CSC support found:
- `/vendor/bin/secril_config_svc` - Contains CSC handling logic

## Methods to Change CSC

### Method 1: Using Samsung Service Mode (Safest)
This method uses Samsung's built-in service mode to change CSC.

```bash
# Enter Service Mode via dialer
# Dial: *#27663368378#
# Or use ADB:
adb shell am start -n com.sec.android.app.servicemodeapp/.ServiceModeApp
```

### Method 2: Direct Property Modification (Requires Root)

**WARNING**: This modifies system properties and requires careful execution.

```bash
#!/bin/bash
# Run this script with root access

# Backup current properties
getprop | grep csc > /sdcard/csc_backup.txt

# Remount system as read-write
mount -o remount,rw /system
mount -o remount,rw /vendor

# Method 2a: Using setprop (temporary, lost after reboot)
setprop ro.csc.sales_code OWO
setprop ril.sales_code OWO
setprop persist.sys.csc_code OWO

# Method 2b: Edit build.prop files (permanent)
# Add or modify these lines in /system/build.prop:
echo "ro.csc.sales_code=OWO" >> /system/build.prop
echo "persist.sys.csc_code=OWO" >> /system/build.prop

# Remount as read-only
mount -o remount,ro /system
mount -o remount,ro /vendor
```

### Method 3: EFS Partition Modification (Advanced)

**CRITICAL WARNING**: Backup EFS before proceeding! Loss of EFS data can brick your device.

```bash
#!/bin/bash
# Backup EFS partition first!
dd if=/dev/block/by-name/efs of=/sdcard/efs_backup.img

# Mount EFS
mount -t ext4 /dev/block/by-name/efs /efs

# Modify sales code files
echo "OWO" > /efs/imei/mps_code.dat
echo "OWO" > /efs/imei/sales_code.dat

# Set correct permissions
chown radio:radio /efs/imei/mps_code.dat
chown radio:radio /efs/imei/sales_code.dat
chmod 0644 /efs/imei/mps_code.dat
chmod 0644 /efs/imei/sales_code.dat

# Sync and unmount
sync
umount /efs
```

### Method 4: Using Odin and CSC Package (Recommended)

This is the safest method using official Samsung tools:

1. Download OWO CSC package for SM-S916B
2. Flash using Odin:
   - Extract firmware
   - Load CSC file in CSC slot
   - Uncheck "Auto Reboot"
   - Flash
3. After flash, factory reset in recovery mode

### Method 5: Multi-CSC Switching (If Multi-CSC ROM)

If the firmware supports Multi-CSC (contains multiple CSC codes):

```bash
#!/bin/bash
# Check if Multi-CSC is available
ls -la /system/csc/

# Find available CSC codes
for csc in /system/csc/*/; do
    echo "Available CSC: $(basename $csc)"
done

# Switch to OWO if available
# This triggers automatic CSC change on next boot
rm -f /efs/imei/mps_code.dat
echo "OWO" > /efs/imei/mps_code.dat
chown radio:radio /efs/imei/mps_code.dat
chmod 0644 /efs/imei/mps_code.dat

# Clear CSC cache
rm -rf /data/csc/*
rm -rf /data/data/com.samsung.android.csc/

# Reboot
reboot
```

## Shell Commands for Analysis

### Check Current CSC
```bash
# Check all CSC-related properties
getprop | grep -i csc
getprop | grep sales

# Check EFS files (requires root)
su
cat /efs/imei/mps_code.dat
cat /efs/imei/sales_code.dat

# Check CSC from build info
getprop ro.product.name
getprop ro.build.product
```

### Verify CSC After Change
```bash
# Verify system properties
getprop ro.csc.sales_code
getprop ril.sales_code
getprop persist.sys.csc_code

# Verify EFS
su
cat /efs/imei/mps_code.dat

# Check CSC app data
ls -la /data/csc/
```

### Force CSC Update
```bash
# Trigger CSC update intent
am broadcast -a com.samsung.intent.action.CSC_UPDATE_TEST

# Clear CSC cache and trigger reload
rm -rf /data/csc/*
pm clear com.android.phone
reboot
```

## Troubleshooting

### CSC Not Changing
1. Check if CSC is hardcoded in modem/baseband
2. Verify EFS partition is writable
3. Ensure all CSC-related properties are updated
4. Try factory reset after modification

### Device Not Booting
1. Restore EFS backup:
   ```bash
   dd if=/sdcard/efs_backup.img of=/dev/block/by-name/efs
   ```
2. Flash stock firmware via Odin

### VoLTE/VoWiFi Not Working
1. Clear IMS configuration:
   ```bash
   rm -rf /data/data/com.sec.imsservice/*
   ```
2. Reset network settings
3. Re-register with network

## Important Notes

1. **ALWAYS backup EFS** before any modification
2. Changing CSC may void warranty
3. Some features may not work with incorrect CSC
4. Network-specific features depend on carrier support
5. Wrong CSC can cause connectivity issues

## Files Modified by This Guide

The following scripts have been added to help with CSC analysis:
- `csc_analysis_tools/analyze_apk.sh` - Analyzes CSC.apk
- `csc_analysis_tools/analyze_binaries.sh` - Analyzes binaries and .so files
- `csc_analysis_tools/analyze_frameworks.sh` - Analyzes framework JARs
- `csc_modification_scripts/change_csc.sh` - Automated CSC change script
- `csc_modification_scripts/backup_efs.sh` - EFS backup script

## References

- CSC.apk decompiled analysis
- Samsung service mode documentation
- Android system properties
- EFS partition structure
