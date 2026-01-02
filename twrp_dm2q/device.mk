# Device Tree for Samsung Galaxy S23+ (dm2q)

LOCAL_PATH := device/samsung/dm2q

# Inherit from common AOSP config
$(call inherit-product, $(SRC_TARGET_DIR)/product/base.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)

# Device identifier
PRODUCT_DEVICE := dm2q
PRODUCT_NAME := twrp_dm2q
PRODUCT_BRAND := Samsung
PRODUCT_MODEL := SM-S916B
PRODUCT_MANUFACTURER := Samsung
PRODUCT_RELEASE_NAME := Samsung Galaxy S23+

# VNDK
PRODUCT_TARGET_VNDK_VERSION := 33

# API
PRODUCT_SHIPPING_API_LEVEL := 33

# Dynamic partitions
PRODUCT_USE_DYNAMIC_PARTITIONS := true

# fastbootd
PRODUCT_PACKAGES += \
    android.hardware.fastboot@1.1-impl-mock \
    fastbootd

# Soong namespaces
PRODUCT_SOONG_NAMESPACES += \
    $(LOCAL_PATH)

# Proprietary files - Samsung/Qualcomm specific (recovery-related only)
# All dependencies analyzed with readelf -d to ensure only recovery-specific blobs
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/proprietary/system/bin/hw/android.hardware.health-service.qti_recovery:$(TARGET_COPY_OUT_RECOVERY)/root/system/bin/hw/android.hardware.health-service.qti_recovery \
    $(LOCAL_PATH)/proprietary/system/lib64/android.hardware.health-V1-ndk.so:$(TARGET_COPY_OUT_RECOVERY)/root/system/lib64/android.hardware.health-V1-ndk.so \
    $(LOCAL_PATH)/proprietary/system/lib64/libhidlbase.so:$(TARGET_COPY_OUT_RECOVERY)/root/system/lib64/libhidlbase.so \
    $(LOCAL_PATH)/proprietary/system/lib64/libdsms.so:$(TARGET_COPY_OUT_RECOVERY)/root/system/lib64/libdsms.so \
    $(LOCAL_PATH)/proprietary/system/lib64/libengmode2lite_recovery.so:$(TARGET_COPY_OUT_RECOVERY)/root/system/lib64/libengmode2lite_recovery.so

# Kernel modules - All Samsung/Qualcomm specific modules
PRODUCT_COPY_FILES += \
    $(call find-copy-subdir-files,*.ko,$(LOCAL_PATH)/proprietary/recovery/root/lib/modules,$(TARGET_COPY_OUT_RECOVERY)/root/lib/modules)

