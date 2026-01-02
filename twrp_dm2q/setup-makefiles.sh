#!/bin/bash
#
# SPDX-FileCopyrightText: 2016 The CyanogenMod Project
# SPDX-FileCopyrightText: 2017-2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

set -e

DEVICE=dm2q
VENDOR=samsung

INITIAL_COPYRIGHT_YEAR=2026

# Load extract_utils and do some sanity checks
MY_DIR="${BASH_SOURCE%/*}"
if [[ ! -d "${MY_DIR}" ]]; then MY_DIR="${PWD}"; fi

ANDROID_ROOT="${MY_DIR}/../../.."

# If we're being sourced by the common script that we called,
# stop right here. No need to go down the rabbit hole.
if [ "${BASH_SOURCE[0]}" != "${0}" ]; then
    return
fi

echo "Setting up makefiles for ${DEVICE}..."
echo ""
echo "Device tree structure is already set up with:"
echo "  - Android.mk"
echo "  - AndroidBoard.mk"
echo "  - BoardConfig.mk"
echo "  - device.mk"
echo "  - twrp_dm2q.mk"
echo "  - omni_dm2q.mk"
echo "  - recovery.fstab"
echo "  - Init rc files (init.recovery.dm2q.rc, init.recovery.qcom.rc, init.recovery.samsung.rc)"
echo "  - VINTF manifests for services"
echo ""
echo "Next steps:"
echo "1. Run extract-files.sh to extract proprietary Samsung/Qualcomm specific files (if needed)"
echo "2. Copy device tree to TWRP source tree: device/samsung/dm2q"
echo "3. Build TWRP with: lunch twrp_dm2q-eng && mka recoveryimage"
echo ""
echo "Setup complete!"
