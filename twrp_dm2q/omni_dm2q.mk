# Omni Device configuration for Samsung Galaxy S23+ (dm2q)

# Inherit from common AOSP config
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from device.mk
$(call inherit-product, device/samsung/dm2q/device.mk)

# Inherit some common Omni stuff
$(call inherit-product, vendor/omni/config/common.mk)

# Device identifier
PRODUCT_DEVICE := dm2q
PRODUCT_NAME := omni_dm2q
PRODUCT_BRAND := Samsung
PRODUCT_MODEL := SM-S916B
PRODUCT_MANUFACTURER := Samsung

PRODUCT_GMS_CLIENTID_BASE := android-samsung

# Build properties
PRODUCT_BUILD_PROP_OVERRIDES += \
    TARGET_DEVICE=dm2q \
    PRODUCT_NAME=dm2qxxx \
    PRIVATE_BUILD_DESC="dm2qxxx-user 13 TP1A.220624.014 S916BXXU5BVL6 release-keys"

BUILD_FINGERPRINT := samsung/dm2qxxx/dm2q:13/TP1A.220624.014/S916BXXU5BVL6:user/release-keys
