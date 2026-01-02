# Device Tree for Samsung Galaxy S23+ (dm2q) - TWRP Configuration

# Inherit from device.mk
$(call inherit-product, device/samsung/dm2q/device.mk)

# Inherit from TWRP product configuration
$(call inherit-product, vendor/twrp/config/common.mk)

# Device identifier
PRODUCT_DEVICE := dm2q
PRODUCT_NAME := twrp_dm2q
PRODUCT_BRAND := Samsung
PRODUCT_MODEL := SM-S916B
PRODUCT_MANUFACTURER := Samsung

# TWRP specific build properties
PRODUCT_BUILD_PROP_OVERRIDES += \
    TARGET_DEVICE=dm2q \
    PRODUCT_NAME=dm2qxxx \
    PRIVATE_BUILD_DESC="dm2qxxx-user 13 TP1A.220624.014 S916BXXU5BVL6 release-keys"

BUILD_FINGERPRINT := samsung/dm2qxxx/dm2q:13/TP1A.220624.014/S916BXXU5BVL6:user/release-keys
