#!/bin/bash
#
# SPDX-FileCopyrightText: 2016 The CyanogenMod Project
# SPDX-FileCopyrightText: 2017-2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

set -e

# Device-specific paths
DEVICE=dm2q
VENDOR=samsung

# Source paths (relative to repository root)
FIRMWARE_ROOT="../"
RECOVERY_ROOT="${FIRMWARE_ROOT}recovery/root"
VENDOR_ROOT="${FIRMWARE_ROOT}vendor"
SYSTEM_ROOT="${FIRMWARE_ROOT}system/system"

# Output directory
PROPRIETARY_DIR="proprietary"

# Create output directories
mkdir -p "${PROPRIETARY_DIR}/system/bin"
mkdir -p "${PROPRIETARY_DIR}/system/lib64"
mkdir -p "${PROPRIETARY_DIR}/system/lib64/hw"
mkdir -p "${PROPRIETARY_DIR}/system/bin/hw"
mkdir -p "${PROPRIETARY_DIR}/recovery/root/lib/modules"

echo "Extracting proprietary files for ${DEVICE}..."

# Function to copy file if it exists
copy_file() {
    local src="$1"
    local dest="$2"
    
    if [ -f "$src" ]; then
        cp -v "$src" "$dest"
    else
        echo "Warning: $src not found"
    fi
}

# Extract recovery libraries
echo "Extracting recovery libraries..."
copy_file "${RECOVERY_ROOT}/system/lib64/android.hardware.boot@1.0.so" "${PROPRIETARY_DIR}/system/lib64/"
copy_file "${RECOVERY_ROOT}/system/lib64/android.hardware.boot@1.1.so" "${PROPRIETARY_DIR}/system/lib64/"
copy_file "${RECOVERY_ROOT}/system/lib64/android.hardware.fastboot@1.0.so" "${PROPRIETARY_DIR}/system/lib64/"
copy_file "${RECOVERY_ROOT}/system/lib64/android.hardware.fastboot@1.1.so" "${PROPRIETARY_DIR}/system/lib64/"
copy_file "${RECOVERY_ROOT}/system/lib64/android.hardware.health@1.0.so" "${PROPRIETARY_DIR}/system/lib64/"
copy_file "${RECOVERY_ROOT}/system/lib64/android.hardware.health@2.0.so" "${PROPRIETARY_DIR}/system/lib64/"

# Extract from system partition
echo "Extracting system libraries..."
copy_file "${SYSTEM_ROOT}/lib64/android.hardware.boot@1.2.so" "${PROPRIETARY_DIR}/system/lib64/"
copy_file "${SYSTEM_ROOT}/lib64/android.hardware.boot-V1-ndk.so" "${PROPRIETARY_DIR}/system/lib64/"
copy_file "${SYSTEM_ROOT}/lib64/android.hardware.health-V1-ndk.so" "${PROPRIETARY_DIR}/system/lib64/"
copy_file "${SYSTEM_ROOT}/lib64/android.hardware.health-V2-ndk.so" "${PROPRIETARY_DIR}/system/lib64/"

# Extract vendor libraries if needed
echo "Extracting vendor libraries..."
if [ -f "${VENDOR_ROOT}/lib64/android.hardware.health@2.1.so" ]; then
    copy_file "${VENDOR_ROOT}/lib64/android.hardware.health@2.1.so" "${PROPRIETARY_DIR}/system/lib64/"
fi

# Extract base libraries
echo "Extracting base system libraries..."
copy_file "${RECOVERY_ROOT}/system/lib64/libbase.so" "${PROPRIETARY_DIR}/system/lib64/"
copy_file "${RECOVERY_ROOT}/system/lib64/libc++.so" "${PROPRIETARY_DIR}/system/lib64/"
copy_file "${RECOVERY_ROOT}/system/lib64/libcutils.so" "${PROPRIETARY_DIR}/system/lib64/"
copy_file "${RECOVERY_ROOT}/system/lib64/liblog.so" "${PROPRIETARY_DIR}/system/lib64/"
copy_file "${RECOVERY_ROOT}/system/lib64/libcrypto.so" "${PROPRIETARY_DIR}/system/lib64/"

# Extract filesystem utilities
echo "Extracting filesystem utilities..."
copy_file "${RECOVERY_ROOT}/system/bin/fsck.f2fs" "${PROPRIETARY_DIR}/system/bin/"
copy_file "${RECOVERY_ROOT}/system/bin/make_f2fs" "${PROPRIETARY_DIR}/system/bin/"
copy_file "${RECOVERY_ROOT}/system/bin/sload_f2fs" "${PROPRIETARY_DIR}/system/bin/"
copy_file "${RECOVERY_ROOT}/system/bin/mke2fs" "${PROPRIETARY_DIR}/system/bin/"
copy_file "${RECOVERY_ROOT}/system/bin/resize2fs" "${PROPRIETARY_DIR}/system/bin/"

# Copy all kernel modules
echo "Copying kernel modules..."
if [ -d "${RECOVERY_ROOT}/lib/modules" ]; then
    cp -rv "${RECOVERY_ROOT}/lib/modules/"*.ko "${PROPRIETARY_DIR}/recovery/root/lib/modules/" 2>/dev/null || true
    echo "Copied $(ls ${RECOVERY_ROOT}/lib/modules/*.ko 2>/dev/null | wc -l) kernel modules"
fi

echo ""
echo "Extraction complete!"
echo "Proprietary files extracted to: ${PROPRIETARY_DIR}"
echo ""
echo "Note: You may need to manually verify and copy additional files"
echo "based on the proprietary-files.txt list."
