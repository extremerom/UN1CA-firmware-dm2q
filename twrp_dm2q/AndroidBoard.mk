#
# Copyright (C) 2026 The TWRP Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

LOCAL_PATH := $(call my-dir)

# Prebuilt kernel
ifeq ($(TARGET_PREBUILT_KERNEL),)
    LOCAL_KERNEL := $(LOCAL_PATH)/prebuilt/kernel
else
    LOCAL_KERNEL := $(TARGET_PREBUILT_KERNEL)
endif

PRODUCT_COPY_FILES += \
    $(LOCAL_KERNEL):kernel

# DTBO image
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/prebuilt/dtbo.img:dtbo.img

# Device tree blobs
PRODUCT_COPY_FILES += \
    $(call find-copy-subdir-files,dtb.*,$(LOCAL_PATH)/prebuilt/dtb,$(TARGET_COPY_OUT_RECOVERY)/root/dtb)

# Recovery init scripts
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/recovery/root/init.recovery.dm2q.rc:$(TARGET_COPY_OUT_RECOVERY)/root/init.recovery.dm2q.rc \
    $(LOCAL_PATH)/recovery/root/init.recovery.qcom.rc:$(TARGET_COPY_OUT_RECOVERY)/root/init.recovery.qcom.rc \
    $(LOCAL_PATH)/recovery/root/init.recovery.samsung.rc:$(TARGET_COPY_OUT_RECOVERY)/root/init.recovery.samsung.rc \
    $(LOCAL_PATH)/recovery/root/ueventd.rc:$(TARGET_COPY_OUT_RECOVERY)/root/ueventd.dm2q.rc

# Recovery fstab
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/recovery.fstab:$(TARGET_COPY_OUT_RECOVERY)/root/system/etc/recovery.fstab

# Health service files
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/recovery/root/system/etc/init/android.hardware.health-service.qti_recovery.rc:$(TARGET_COPY_OUT_RECOVERY)/root/system/etc/init/android.hardware.health-service.qti_recovery.rc \
    $(LOCAL_PATH)/recovery/root/system/etc/vintf/manifest/android.hardware.health-service.qti.xml:$(TARGET_COPY_OUT_RECOVERY)/root/system/etc/vintf/manifest/android.hardware.health-service.qti.xml
