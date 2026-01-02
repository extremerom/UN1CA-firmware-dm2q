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

ifeq ($(TARGET_DEVICE),dm2q)

# Qualcomm Health Service Binary
include $(CLEAR_VARS)
LOCAL_MODULE := android.hardware.health-service.qti_recovery
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_MODULE_TAGS := optional
LOCAL_SRC_FILES := proprietary/system/bin/hw/$(LOCAL_MODULE)
LOCAL_MODULE_PATH := $(TARGET_RECOVERY_ROOT_OUT)/system/bin/hw
include $(BUILD_PREBUILT)

# Qualcomm Health HAL Library (AIDL V1)
include $(CLEAR_VARS)
LOCAL_MODULE := android.hardware.health-V1-ndk
LOCAL_MODULE_CLASS := SHARED_LIBRARIES
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_SUFFIX := .so
LOCAL_SRC_FILES_64 := proprietary/system/lib64/$(LOCAL_MODULE)$(LOCAL_MODULE_SUFFIX)
LOCAL_MULTILIB := 64
LOCAL_MODULE_PATH := $(TARGET_RECOVERY_ROOT_OUT)/system/lib64
include $(BUILD_PREBUILT)

# HIDL Base Library
include $(CLEAR_VARS)
LOCAL_MODULE := libhidlbase
LOCAL_MODULE_CLASS := SHARED_LIBRARIES
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_SUFFIX := .so
LOCAL_SRC_FILES_64 := proprietary/system/lib64/$(LOCAL_MODULE)$(LOCAL_MODULE_SUFFIX)
LOCAL_MULTILIB := 64
LOCAL_MODULE_PATH := $(TARGET_RECOVERY_ROOT_OUT)/system/lib64
include $(BUILD_PREBUILT)

# Samsung DSMS Library
include $(CLEAR_VARS)
LOCAL_MODULE := libdsms
LOCAL_MODULE_CLASS := SHARED_LIBRARIES
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_SUFFIX := .so
LOCAL_SRC_FILES_64 := proprietary/system/lib64/$(LOCAL_MODULE)$(LOCAL_MODULE_SUFFIX)
LOCAL_MULTILIB := 64
LOCAL_MODULE_PATH := $(TARGET_RECOVERY_ROOT_OUT)/system/lib64
include $(BUILD_PREBUILT)

# Samsung Engineering Mode Lite Recovery Library
include $(CLEAR_VARS)
LOCAL_MODULE := libengmode2lite_recovery
LOCAL_MODULE_CLASS := SHARED_LIBRARIES
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_SUFFIX := .so
LOCAL_SRC_FILES_64 := proprietary/system/lib64/$(LOCAL_MODULE)$(LOCAL_MODULE_SUFFIX)
LOCAL_MULTILIB := 64
LOCAL_MODULE_PATH := $(TARGET_RECOVERY_ROOT_OUT)/system/lib64
include $(BUILD_PREBUILT)

endif
