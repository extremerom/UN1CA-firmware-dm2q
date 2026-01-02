# Extracted IMG Partitions

This repository contains extracted content from Android boot partition images for the UN1CA firmware (dm2q device).

## Extracted Partitions

### 1. boot/ - Boot Partition
Contains the main kernel and boot configuration:
- **kernel** (45.7 MB) - Linux kernel 5.15.178
- **kernel_configs.txt** - Kernel configuration
- **kernel_version.txt** - Kernel version info
- **boot.json** - Boot image metadata
- **boot.avb.json** - Android Verified Boot info

### 2. recovery/ - Recovery Partition
Contains recovery kernel and ramdisk filesystem:
- **kernel** (44 MB) - Recovery kernel 5.15.178
- **root/** - Recovery ramdisk filesystem with init scripts, modules, and recovery tools
- **dtb** files - Device tree blobs (4 variants)
- **recoveryDtbo** - Recovery device tree overlay
- **recovery.json** - Recovery image metadata
- **recovery.avb.json** - AVB verification info

The recovery/root filesystem includes:
- Init scripts (init.recovery.qcom.rc, init.recovery.samsung.rc)
- Kernel modules in lib/modules/ (msm_drm.ko and others)
- SELinux policies
- File contexts for all partitions

### 3. vendor_boot/ - Vendor Boot Partition
Contains vendor-specific boot components:
- **root.1/** - Vendor ramdisk filesystem with first stage ramdisk and kernel modules
- **dtb** files - Device tree blobs (4 variants with decompiled sources)
- **bootconfig** - Boot configuration parameters
- **vendor_boot.json** - Vendor boot metadata
- **vendor_boot.avb.json** - AVB verification info

The vendor_boot/root.1 filesystem includes:
- first_stage_ramdisk/ - Early boot ramdisk
- lib/modules/ - Over 400 kernel modules including Samsung-specific and Qualcomm drivers

### 4. dtbo/ - Device Tree Blob Overlay Partition
Contains device tree overlays:
- **dt/** directory with 9 device tree blobs (dt.0 through dt.8)
- Each blob includes:
  - .dtb - Binary device tree blob
  - .dts - Decompiled device tree source
  - .dts.yaml - YAML representation
- **dtbo.json** - DTBO metadata
- **dtbo.avb.json** - AVB verification info

## File Permissions
All files have been extracted with preserved permissions:
- Executable files (.ko modules, scripts): mode 755
- Configuration files: mode 644
- Symlinks preserved as-is

## AVB (Android Verified Boot)
All partitions include AVB signature information showing they are signed with release keys.

## Tools Used
- Android Boot Image Editor (cfig/Android_boot_image_editor)
- Device Tree Compiler (dtc)
- Git LFS for large kernel files

## Source Images
Downloaded from Dropbox (not included in repository):
- boot.img (96 MB)
- recovery.img (104 MB)
- vendor_boot.img (96 MB)
- dtbo.img (16 MB)

These source .img files are excluded via .gitignore as only the extracted content is needed.
