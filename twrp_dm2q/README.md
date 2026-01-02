# TWRP Device Tree for Samsung Galaxy S23+ (dm2q)

This is a Team Win Recovery Project (TWRP) device tree for the Samsung Galaxy S23+ (SM-S916B, codename: dm2q) based on the UN1CA firmware dump.

## Device Specifications

| Device       | Samsung Galaxy S23+                         |
| -----------: | :------------------------------------------ |
| SoC          | Qualcomm Snapdragon 8 Gen 2 (SM8550)        |
| Platform     | kalama                                       |
| CPU          | Octa-core Kryo                              |
| GPU          | Adreno 740                                  |
| Memory       | 8GB RAM                                     |
| Shipped Android Version | 13                               |
| Storage      | 256GB / 512GB                               |
| Battery      | Non-removable Li-Po 4700 mAh                |
| Display      | 6.6" 1080x2340 AMOLED, 120 Hz               |
| Camera (Back)| 50 MP (main), 12 MP (ultrawide), 10 MP (telephoto) |
| Camera (Front)| 12 MP                                      |

## Build Information

- **Kernel Version:** 5.15.178
- **Android Version:** 13
- **Security Patch:** 2025-12-00
- **Build Number:** S916BXXU5BVL6
- **Board:** SRPVH05B008

## Device Tree Structure

```
twrp_dm2q/
├── Android.mk                   # Android build system entry point
├── AndroidBoard.mk              # Board-specific build rules
├── AndroidProducts.mk           # Build system configuration
├── BoardConfig.mk               # Board and kernel configuration
├── device.mk                    # Device-specific makefiles
├── twrp_dm2q.mk                # TWRP product configuration
├── omni_dm2q.mk                # Alternative Omni configuration
├── recovery.fstab              # Recovery partition table
├── proprietary-files.txt       # List of proprietary blobs
├── proprietary-files.mk        # Makefile for proprietary blobs
├── extract-files.sh            # Script to extract proprietary files
├── setup-makefiles.sh          # Setup script for build system
├── prebuilt/                   # Prebuilt binaries
│   ├── kernel                  # Precompiled kernel (45.7 MB)
│   ├── dtbo.img               # Device Tree Blob Overlay (16 MB)
│   └── dtb/                   # Device Tree Blobs (4 variants + sources)
│       ├── dtb.0              # Binary device tree blob
│       ├── dtb.0.dts          # Decompiled source
│       ├── dtb.0.dts.yaml     # YAML representation
│       ├── dtb.1
│       ├── dtb.2
│       └── dtb.3
├── proprietary/               # Proprietary Samsung/Qualcomm blobs
│   ├── system/
│   │   ├── bin/hw/           # Hardware service binaries
│   │   │   └── android.hardware.health-service.qti_recovery
│   │   └── lib64/            # 64-bit libraries
│   │       ├── libdsms.so
│   │       └── libengmode2lite_recovery.so
│   └── recovery/root/lib/modules/  # 425 kernel modules (.ko files)
└── recovery/root/             # Recovery ramdisk files
    ├── init.recovery.dm2q.rc      # Device-specific init
    ├── init.recovery.qcom.rc      # Qualcomm platform init
    ├── init.recovery.samsung.rc   # Samsung-specific init
    ├── ueventd.rc                 # Device event rules
    └── system/etc/
        ├── init/
        │   └── android.hardware.health-service.qti_recovery.rc
        └── vintf/manifest/
            └── android.hardware.health-service.qti.xml
```

## Kernel and DTB Sources

### Kernel
- **Source:** `boot/kernel` from UN1CA firmware dump
- **Size:** 45,750,784 bytes (44 MB)
- **Version:** 5.15.178
- **Location:** `twrp_dm2q/prebuilt/kernel`

### Device Tree Blobs (DTB)
- **Source:** `recovery/dtb*` from UN1CA firmware dump
- **Count:** 4 device tree blob variants
- **Location:** `twrp_dm2q/prebuilt/dtb/`

### Device Tree Blob Overlay (DTBO)
- **Source:** `kernel/dtbo.img` from UN1CA firmware dump
- **Size:** 16,777,216 bytes (16 MB)
- **Location:** `twrp_dm2q/prebuilt/dtbo.img`

## Required Blobs and Libraries

Only Samsung/Qualcomm device-specific proprietary blobs are included. Standard AOSP/TWRP components (recovery binary, basic utilities, base libraries) are built from TWRP source.

### Proprietary Components Included:

#### Qualcomm Health Service
- **Binary:** `android.hardware.health-service.qti_recovery`
- **Location:** `proprietary/system/bin/hw/`
- **Purpose:** Qualcomm-specific health monitoring service for recovery
- **Init file:** `android.hardware.health-service.qti_recovery.rc`
- **VINTF manifest:** `android.hardware.health-service.qti.xml`

#### Samsung-specific Libraries
- **libdsms.so** - Samsung Device Security Management Service library
- **libengmode2lite_recovery.so** - Samsung Engineering Mode for recovery (281 KB)
- **Location:** `proprietary/system/lib64/`

#### Kernel Modules
- **Count:** 425 kernel modules (.ko files)
- **Source:** Copied from `recovery/root/lib/modules/`
- **Location:** `proprietary/recovery/root/lib/modules/*.ko`
- **Types:**
  - Samsung ABC modules (abc.ko, abc_hub.ko)
  - Samsung sensors (adsp_*.ko, slpi_*.ko)
  - Samsung factory modules (*_factory_module.ko)
  - Qualcomm platform drivers (msm_*.ko, qcom_*.ko)
  - Display drivers (msm_drm.ko, samsung_*.ko)
  - Network drivers (cfg80211.ko, mac80211.ko, qca_cld3_*.ko)
  - Storage drivers (ufs_*.ko, scsi_*.ko)
  - Power management (bcl_*.ko, thermal_*.ko)
  - Security modules (hdcp_*.ko, sec_*.ko)

See the complete list in `DEVICE_TREE_FILES_REPORT.md` in the repository root.

### Init and Configuration Files

#### Init RC Files
- **init.recovery.dm2q.rc** - Device-specific recovery initialization
  - Samsung EFS partition setup
  - Samsung ODE partitions (keydata, keyrefuge)
  - Backlight control configuration
  - USB configuration for recovery mode
  - Battery charging settings
  
- **init.recovery.qcom.rc** - Qualcomm platform initialization
  - USB controller configuration
  - Backlight brightness setup
  - Platform-specific device nodes

- **init.recovery.samsung.rc** - Samsung-specific initialization
  - EFS partition handling
  - Battery charging path configuration

- **ueventd.rc** - Device event rules
  - Block device permissions
  - Samsung partition permissions (EFS, ODE, carrier)
  - UFS device nodes
  - Graphics and input device permissions

#### VINTF Manifest
- **android.hardware.health-service.qti.xml**
  - Declares Qualcomm health HAL service for recovery
  - AIDL interface version 1
  - Required for proper health monitoring in TWRP

## Partitions

### Dynamic Partitions
The device uses dynamic partitions with a super partition:

- **Super Partition Size:** 12,664,700,928 bytes (~11.8 GB)
- **Dynamic Partitions Group:** qti_dynamic_partitions
- **Group Size:** 12,660,506,624 bytes
- **Partitions in Group:** system, system_ext, product, vendor, odm, vendor_dlkm, system_dlkm

### Key Partition Sizes
- **Boot:** 100,663,296 bytes (~96 MB)
- **Recovery:** 109,051,904 bytes (~104 MB)
- **DTBO:** 16,777,216 bytes (16 MB)
- **Vendor Boot:** 100,663,296 bytes (~96 MB)

## Recovery Features (TWRP Configuration)

- Portrait HDPI theme
- Brightness control support
- Download mode support (Samsung)
- NTFS support
- USB mounting
- Multiple language support
- Android 13 FBE decryption support
- Qualcomm FBE decryption support
- Dynamic partition support
- F2FS and EXT4 support
- Repack tools included

## Building TWRP

1. Set up TWRP build environment
2. Clone this device tree to `device/samsung/dm2q`
3. Clone the necessary vendor blobs (reference the proprietary-files.txt)
4. Run:
```bash
. build/envsetup.sh
lunch twrp_dm2q-eng
mka recoveryimage
```

## Firmware Source

This device tree is based on the UN1CA firmware dump for the Samsung Galaxy S23+ (dm2q).

**Repository:** https://github.com/extremerom/UN1CA-firmware-dm2q

The firmware dump includes:
- Extracted boot images (boot, recovery, vendor_boot, dtbo)
- All system partitions (system, vendor, product, odm, etc.)
- Kernel modules and drivers
- Recovery ramdisk with all necessary files

## Notes

### Boot Image Header
- Header Version: 4 (for boot.img), 2 (for recovery.img)
- Page Size: 4096 bytes
- Kernel offset: 0x00008000
- Ramdisk offset: 0x02000000
- Tags offset: 0x01e00000
- DTB offset: 0x01f00000

### USB Controller
- Controller: a600000.dwc3
- Mode: Peripheral (for recovery)

### Encryption
The device supports File-Based Encryption (FBE) with hardware-backed keystore.
TWRP is configured to attempt FBE metadata decryption.

### Samsung-specific Features
- Download mode available (instead of fastboot/bootloader mode)
- Samsung ODE support (keydata and keyrefuge partitions)
- Samsung-specific partitions: prism, optics, carrier, efs, sec_efs

## Credits

- **Firmware Source:** extremerom/UN1CA-firmware-dm2q
- **Device Tree Creator:** Generated from UN1CA firmware dump
- **TWRP:** Team Win Recovery Project
- **Base Reference:** android_device_samsung_pa1q (for file structure reference)

## License

This device tree inherits the licensing from the source firmware components and TWRP.

## Maintainer

UN1CA-firmware-dm2q project

---

**Last Updated:** 2026-01-02
**Firmware Version:** S916BXXU5BVL6 (December 2025 security patch)
