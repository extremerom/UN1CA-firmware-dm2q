# CSC Analysis and Modification Tools

This repository contains tools and documentation for analyzing and modifying the CSC (Country-Specific Code) on Samsung Galaxy S23+ (SM-S916B) firmware.

## Problem Statement

Change the CSC permanently from `TPA` to `OWO` on device:
- **Model**: SM-S916B (Galaxy S23+)
- **Current CSC**: SAOMC_SM-S916B_OWO_TPA_16_0009 TPA/TPA,TPA/TPA
- **Target CSC**: OWO

## Repository Structure

```
.
├── csc_analysis_tools/          # Analysis scripts for firmware components
│   ├── analyze_apk.sh          # Analyze APK files for CSC references
│   ├── analyze_binaries.sh     # Analyze binaries and .so libraries
│   └── analyze_frameworks.sh   # Analyze framework JARs
│
├── csc_modification_scripts/    # Scripts to modify CSC
│   ├── backup_efs.sh           # Backup EFS partition (CRITICAL!)
│   ├── change_csc.sh           # Change CSC from TPA to OWO
│   └── check_csc.sh            # Verify current CSC configuration
│
├── CSC_MODIFICATION_GUIDE.md   # Comprehensive modification guide
└── README.md                   # This file
```

## Prerequisites

### On Device
- Samsung Galaxy S23+ (SM-S916B)
- **Root access** (required for CSC modification)
- USB debugging enabled
- ~500MB free space on internal storage for backups

### On Computer
- ADB (Android Debug Bridge) installed
- `apktool` for APK analysis (installed automatically)
- Linux or macOS recommended (Windows with WSL also works)

## Quick Start

### 1. Install Required Tools

The analysis scripts require `apktool`:
```bash
sudo apt update
sudo apt install apktool -y
```

### 2. Run Analysis Tools

Analyze the firmware components:

```bash
# Make scripts executable
chmod +x csc_analysis_tools/*.sh

# Analyze CSC.apk
./csc_analysis_tools/analyze_apk.sh

# Analyze binaries and libraries
./csc_analysis_tools/analyze_binaries.sh

# Analyze framework JARs
./csc_analysis_tools/analyze_frameworks.sh
```

### 3. Backup EFS Partition (CRITICAL!)

**WARNING**: Never modify CSC without backing up EFS first!

```bash
# Connect device via ADB
adb devices

# Push backup script to device
adb push csc_modification_scripts/backup_efs.sh /sdcard/

# Execute backup script on device
adb shell "su -c 'sh /sdcard/backup_efs.sh'"

# Pull backup to computer (IMPORTANT!)
adb pull /sdcard/CSC_Backup_* ./backups/
```

### 4. Check Current CSC

```bash
# Push check script to device
adb push csc_modification_scripts/check_csc.sh /sdcard/

# Run check script
adb shell "su -c 'sh /sdcard/check_csc.sh'"
```

### 5. Change CSC

```bash
# Push change script to device
adb push csc_modification_scripts/change_csc.sh /sdcard/

# Run CSC change script
adb shell "su -c 'sh /sdcard/change_csc.sh'"

# Reboot device
adb reboot
```

### 6. Verify Change

After reboot:
```bash
# Check if CSC changed
adb shell "getprop ro.csc.sales_code"
adb shell "getprop ril.sales_code"
adb shell "su -c 'cat /efs/imei/mps_code.dat'"
```

## Analysis Results

### Key Findings

#### 1. CSC Storage Locations
CSC information is stored in multiple locations:

**System Properties:**
- `ro.csc.sales_code` - Main CSC code (read-only)
- `ril.sales_code` - RIL (Radio Interface Layer) sales code
- `persist.sys.csc_code` - Persistent CSC code

**EFS Partition:**
- `/efs/imei/mps_code.dat` - Multi-CSC code
- `/efs/imei/sales_code.dat` - Sales code

**System Files:**
- `/system/priv-app/CSC/CSC.apk` - CSC management app
- `/system/csc/` - Multi-CSC configurations (if available)

#### 2. CSC-Related Binaries
Found in `vendor/bin/`:
- `secril_config_svc` - Contains CSC handling logic
- References to `ro.csc.sales_code` in RIL configuration

#### 3. CSC.apk Analysis
Decompiled CSC.apk reveals:
- CSC Ringtone Manager - reads `ro.csc.sales_code`
- CSC Compare Service - monitors CSC changes
- CSC Update Service - handles CSC updates
- Broadcast receivers for CSC update intents

## Modification Methods

### Method 1: EFS Modification (Recommended for Root Users)
Directly modify EFS partition files. See `change_csc.sh` script.

**Pros:**
- Works with root access
- Permanent change
- No firmware flash needed

**Cons:**
- Requires careful execution
- Must backup EFS first
- May require factory reset

### Method 2: Odin Flash (Safest)
Flash official OWO CSC package using Odin.

**Pros:**
- Official Samsung method
- Safest approach
- Includes all carrier configurations

**Cons:**
- Requires downloading full CSC package
- May trigger Knox counter
- Wipes user data

### Method 3: Multi-CSC Switching
If firmware supports Multi-CSC, switch between included codes.

**Pros:**
- Built-in support
- Automatic configuration
- No firmware modification

**Cons:**
- Only works if OWO is included in Multi-CSC
- May not be available on all firmwares

## Safety Warnings

⚠️ **CRITICAL WARNINGS** ⚠️

1. **ALWAYS backup EFS partition before any modification**
   - Loss of EFS can permanently brick your device
   - Keep multiple backups in safe locations

2. **Changing CSC may:**
   - Void your warranty
   - Trigger Samsung Knox
   - Cause network connectivity issues
   - Break carrier-specific features

3. **Wrong CSC can cause:**
   - VoLTE/VoWiFi not working
   - Mobile data issues
   - SMS/MMS problems
   - Emergency calling issues

4. **Test after modification:**
   - Voice calls
   - Mobile data
   - SMS/MMS
   - Emergency calls
   - VoLTE/VoWiFi

## Troubleshooting

### CSC Not Changing
1. Verify EFS files were modified: `cat /efs/imei/mps_code.dat`
2. Clear CSC cache: `rm -rf /data/csc/*`
3. Factory reset (will erase data!)
4. Flash OWO CSC via Odin

### Device Not Booting
1. Boot to recovery mode
2. Wipe cache partition
3. If still not booting, restore EFS backup
4. Last resort: Flash stock firmware

### Network Issues
1. Reset network settings
2. Re-insert SIM card
3. Check APN settings
4. Verify CSC matches carrier requirements

## Technical Details

For detailed technical information, see [CSC_MODIFICATION_GUIDE.md](CSC_MODIFICATION_GUIDE.md).

## Analysis Scripts Details

### analyze_apk.sh
- Decompiles APK files using apktool
- Searches for CSC-related strings in smali code
- Identifies property access patterns
- Analyzes AndroidManifest.xml for CSC intents

### analyze_binaries.sh
- Uses `readelf` to analyze ELF binaries
- Uses `strings` to extract readable strings
- Searches for CSC and sales_code references
- Analyzes .so libraries for CSC handling

### analyze_frameworks.sh
- Analyzes framework JAR files
- Searches for CSC-related classes
- Identifies CSC API usage

## Contributing

This is an analysis and modification toolset for a specific device. Contributions should:
- Maintain device safety
- Include proper warnings
- Test on target device
- Document all changes

## Disclaimer

**USE AT YOUR OWN RISK**

- These tools modify critical system files
- Improper use can brick your device
- Author is not responsible for any damage
- Always maintain backups
- Ensure you have recovery method available

## License

This project is for educational and personal use only. Samsung, Galaxy, and related trademarks are property of Samsung Electronics.

## Support

For issues or questions:
1. Read the CSC_MODIFICATION_GUIDE.md thoroughly
2. Check troubleshooting section
3. Verify you have proper backups
4. Ensure root access is working

## Version History

- **v1.0** (2024-12-28)
  - Initial release
  - CSC analysis tools
  - EFS backup script
  - CSC modification script
  - Comprehensive documentation
