# Análisis de Bibliotecas y Configuraciones: dm2q vs r0q

## Resumen

Este documento analiza las **bibliotecas (.so)** y **archivos de configuración (etc/)** que son únicos a cada dispositivo.

---

## 1. BIBLIOTECAS EN system/lib/ Y system/lib64/ ÚNICOS A dm2q

### Bibliotecas 32-bit (system/lib/)

- `system/lib/FrcMcWrapper.so`
- `system/lib/android.hardware.security.keymint-V2-ndk.so`
- `system/lib/libFrucPSVTLib.so`
- `system/lib/libSemanticMap_v1.camera.samsung.so`
- `system/lib/libSlowShutter-core.so`
- `system/lib/libaifrc.aidl.quram.so`
- `system/lib/libaifrcInterface.camera.samsung.so`
- `system/lib/libmcaimegpu.samsung.so`
- `system/lib/libsec_semAidl.so`
- `system/lib/libsec_skpmAidl.so`
- `system/lib/libswdapaidl.so`
- `system/lib/libswspatializeraidl.so`
- `system/lib/libtflite_uwb_jni.so`
- `system/lib/vendor.samsung.hardware.frcmc-V1-ndk.so`
- `system/lib/vendor.samsung.hardware.keymint-V2-ndk.so`
- `system/lib/vendor.samsung.hardware.security.sem-V1-ndk.so`
- `system/lib/vendor.samsung.hardware.security.skpm-V1-ndk.so`

### Bibliotecas 64-bit (system/lib64/)

- `system/lib64/FrcMcWrapper.so`
- `system/lib64/android.hardware.security.keymint-V2-ndk.so`
- `system/lib64/libDocDeblur.camera.samsung.so`
- `system/lib64/libDocObjectRemoval.camera.samsung.so`
- `system/lib64/libDocObjectRemoval.enhanceX.samsung.so`
- `system/lib64/libFrucPSVTLib.so`
- `system/lib64/libSceneDetector_v1.camera.samsung.so`
- `system/lib64/libSemanticMap_v1.camera.samsung.so`
- `system/lib64/libSlowShutter-core.so`
- `system/lib64/libWideDistortionCorrection.camera.samsung.so`
- `system/lib64/libacz_hhdr.arcsoft.so`
- `system/lib64/libaiclearzoom_raw.arcsoft.so`
- `system/lib64/libaiclearzoomraw_wrapper_v1.camera.samsung.so`
- `system/lib64/libaifrc.aidl.quram.so`
- `system/lib64/libaifrcInterface.camera.samsung.so`
- `system/lib64/libface_recognition.arcsoft.so`
- `system/lib64/libmcaimegpu.samsung.so`
- `system/lib64/libmediacaptureservice.so`
- `system/lib64/libmediaplayerservice.so`
- `system/lib64/libpic_best.arcsoft.so`
- `system/lib64/libsec_semAidl.so`
- `system/lib64/libsec_skpmAidl.so`
- `system/lib64/libstagefright_httplive_sec.so`
- `system/lib64/libswdapaidl.so`
- `system/lib64/libswspatializeraidl.so`
- `system/lib64/libtflite_uwb_jni.so`
- `system/lib64/vendor.samsung.hardware.frcmc-V1-ndk.so`
- `system/lib64/vendor.samsung.hardware.keymint-V2-ndk.so`
- `system/lib64/vendor.samsung.hardware.security.sem-V1-ndk.so`
- `system/lib64/vendor.samsung.hardware.security.skpm-V1-ndk.so`

---

## 2. BIBLIOTECAS EN system/lib/ Y system/lib64/ ÚNICOS A r0q

### Bibliotecas 32-bit (system/lib/)

- `system/lib/android.hardware.security.keymint-V1-ndk.so`
- `system/lib/libmdfpp_req.so`
- `system/lib/libmediacaptureservice.so`
- `system/lib/libmediaplayerservice.so`
- `system/lib/libsdp_crypto.so`
- `system/lib/libsdp_kekm.so`
- `system/lib/libsdp_sdk.so`
- `system/lib/libsec_semHal.so`
- `system/lib/libsec_skpmHal.so`
- `system/lib/libstagefright_httplive_sec.so`
- `system/lib/vendor.samsung.hardware.keymint-V1-ndk.so`
- `system/lib/vendor.samsung.hardware.security.sem@1.0.so`
- `system/lib/vendor.samsung.hardware.security.skpm@1.0.so`

### Bibliotecas 64-bit (system/lib64/)

- `system/lib64/android.hardware.dumpstate@1.0.so`
- `system/lib64/android.hardware.dumpstate@1.1.so`
- `system/lib64/android.hardware.security.keymint-V1-ndk.so`
- `system/lib64/libHREnhancementAPI.camera.samsung.so`
- `system/lib64/libarcsoft_superresolution_bokeh.so`
- `system/lib64/libhigh_dynamic_range.arcsoft.so`
- `system/lib64/libhighres_enhancement.arcsoft.so`
- `system/lib64/liblow_light_hdr.arcsoft.so`
- `system/lib64/libmdfpp_req.so`
- `system/lib64/libsdp_crypto.so`
- `system/lib64/libsdp_kekm.so`
- `system/lib64/libsdp_sdk.so`
- `system/lib64/libsec_semHal.so`
- `system/lib64/libsec_skpmHal.so`
- `system/lib64/vendor.samsung.hardware.keymint-V1-ndk.so`
- `system/lib64/vendor.samsung.hardware.security.sem@1.0.so`
- `system/lib64/vendor.samsung.hardware.security.skpm@1.0.so`

---

## 3. ARCHIVOS DE CONFIGURACIÓN etc/ ÚNICOS A dm2q

- `system/etc/default-permissions/default-permissions-com.samsung.mediasearch.xml`
- `system/etc/default-permissions/default-permissions-com.samsung.videoscan.xml`
- `system/etc/init/digitalkey_init_uwb_tss2.rc`
- `system/etc/init/init.system.uwb.rc`
- `system/etc/init/ssu_dm2qxxx.rc`
- `system/etc/libuwb-cal.conf`
- `system/etc/mediasearch`
- `system/etc/mediasearch/data`
- `system/etc/mediasearch/data/dec_adaptor.tflite`
- `system/etc/mediasearch/data/dec_event.tflite`
- `system/etc/mediasearch/data/enc_image.tflite`
- `system/etc/mediasearch/data/enc_text.tflite`
- `system/etc/mediasearch/data/versioninfo.json`
- `system/etc/permissions/com.samsung.android.uwb_extras.xml`
- `system/etc/permissions/com.sec.feature.pocketsensitivitymode_level1.xml`
- `system/etc/permissions/org.carconnectivity.android.digitalkey.timesync.xml`
- `system/etc/permissions/privapp-permissions-com.samsung.android.dcktimesync.xml`
- `system/etc/permissions/privapp-permissions-com.samsung.mediasearch.xml`
- `system/etc/permissions/privapp-permissions-com.samsung.videoscan.xml`
- `system/etc/permissions/privapp-permissions-com.sec.android.app.uwbtest.xml`
- `system/etc/pp_model.tflite`
- `system/etc/saiv`
- `system/etc/saiv/image_understanding`
- `system/etc/saiv/image_understanding/db`
- `system/etc/saiv/image_understanding/db/aic_classifier`
- `system/etc/saiv/image_understanding/db/aic_classifier/aic_classifier_cnn.info`
- `system/etc/saiv/image_understanding/db/aic_detector`
- `system/etc/saiv/image_understanding/db/aic_detector/aic_detector_cnn.info`

---

## 4. ARCHIVOS DE CONFIGURACIÓN etc/ ÚNICOS A r0q

- `system/etc/default-permissions/default-permissions-com.sec.factory.cameralyzer.xml`
- `system/etc/init/digitalkey_init_ble_tss2.rc`
- `system/etc/init/rscmgr.rc`
- `system/etc/init/sdp_cryptod.rc`
- `system/etc/init/ssu_r0qxxx.rc`
- `system/etc/permissions/com.sec.feature.cover.ledbackcover.xml`
- `system/etc/permissions/com.sec.feature.cover.nfcledcover.xml`
- `system/etc/permissions/com.sec.feature.pocketmode_level33.xml`
- `system/etc/permissions/privapp-permissions-com.samsung.unifiedtp.xml`
- `system/etc/permissions/privapp-permissions-com.sec.android.cover.ledcover.xml`

---

## 5. BIBLIOTECAS EN system_ext/lib/ Y system_ext/lib64/ ÚNICOS A dm2q

### Bibliotecas 32-bit (system_ext/lib/)

- `system_ext/lib/libqcc.so`
- `system_ext/lib/libqcc_file_agent_sys.so`
- `system_ext/lib/libqccdme.so`
- `system_ext/lib/libqccfileservice.so`
- `system_ext/lib/vendor.qti.hardware.qccsyshal@1.0.so`
- `system_ext/lib/vendor.qti.hardware.qccsyshal@1.1.so`
- `system_ext/lib/vendor.qti.hardware.qccsyshal@1.2.so`
- `system_ext/lib/vendor.qti.hardware.qccvndhal@1.0.so`
- `system_ext/lib/vendor.qti.qccsyshal_aidl-V1-ndk.so`
- `system_ext/lib/vendor.qti.qccvndhal_aidl-V1-ndk.so`

### Bibliotecas 64-bit (system_ext/lib64/)

- `system_ext/lib64/libqcc.so`
- `system_ext/lib64/libqcc_file_agent_sys.so`
- `system_ext/lib64/libqccdme.so`
- `system_ext/lib64/libqccfileservice.so`
- `system_ext/lib64/vendor.qti.hardware.qccsyshal@1.0.so`
- `system_ext/lib64/vendor.qti.hardware.qccsyshal@1.1.so`
- `system_ext/lib64/vendor.qti.hardware.qccsyshal@1.2-halimpl.so`
- `system_ext/lib64/vendor.qti.hardware.qccsyshal@1.2.so`
- `system_ext/lib64/vendor.qti.hardware.qccvndhal@1.0.so`
- `system_ext/lib64/vendor.qti.qccsyshal_aidl-V1-ndk.so`
- `system_ext/lib64/vendor.qti.qccsyshal_aidl-halimpl.so`
- `system_ext/lib64/vendor.qti.qccvndhal_aidl-V1-ndk.so`

---

## 6. ARCHIVOS DE CONFIGURACIÓN etc/ EN system_ext/ ÚNICOS A dm2q

- `system_ext/etc/init/vendor.qti.hardware.qccsyshal@1.2-service.rc`
- `system_ext/etc/init/vendor.qti.qccsyshal_aidl-service.rc`
- `system_ext/etc/vintf/manifest/vendor.qti.qccsyshal_aidl-service.xml`

---

Análisis completado
