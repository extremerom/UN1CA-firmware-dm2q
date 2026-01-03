# Archivos a COPIAR de dm2q a r0q

Esta lista contiene TODOS los archivos que debes copiar de dm2q a r0q para el porteo.

---

## CRÍTICOS - DEBEN COPIARSE SÍ O SÍ

### 1. Partición vendor/ COMPLETA
```
vendor/
```
**Copia TODA la partición vendor de dm2q**

### 2. Kernel y Boot
```
boot.img
dtbo.img
vendor_boot.img
init_boot.img
```

### 3. Archivos de configuración
```
fs_config-system
fs_config-system_ext
fs_config-product
fs_config-vendor
fs_config-odm
fs_config-system_dlkm
fs_config-vendor_dlkm

file_context-system
file_context-system_ext
file_context-product
file_context-vendor
file_context-odm
file_context-system_dlkm
file_context-vendor_dlkm

system/dpolicy_system
```

---

## SYSTEM_EXT/ - 41 archivos CRÍTICOS

### VNDK Android 13
```
system_ext/apex/com.android.vndk.v33.apex
```

### QCC (Qualcomm Car Connectivity) - 6 componentes principales
```
system_ext/app/QCC
system_ext/app/QCC/QCC.apk

system_ext/bin/qccsyshal@1.2-service
system_ext/bin/qccsyshal_aidl-service

system_ext/etc/init/vendor.qti.hardware.qccsyshal@1.2-service.rc
system_ext/etc/init/vendor.qti.qccsyshal_aidl-service.rc

system_ext/etc/vintf/manifest/vendor.qti.qccsyshal_aidl-service.xml

system_ext/framework/org.carconnectivity.android.digitalkey.timesync.jar
```

### Bibliotecas QCC 32-bit
```
system_ext/lib/libqcc.so
system_ext/lib/libqcc_file_agent_sys.so
system_ext/lib/libqccdme.so
system_ext/lib/libqccfileservice.so
system_ext/lib/vendor.qti.hardware.qccsyshal@1.0.so
system_ext/lib/vendor.qti.hardware.qccsyshal@1.1.so
system_ext/lib/vendor.qti.hardware.qccsyshal@1.2.so
system_ext/lib/vendor.qti.hardware.qccvndhal@1.0.so
system_ext/lib/vendor.qti.qccsyshal_aidl-V1-ndk.so
system_ext/lib/vendor.qti.qccvndhal_aidl-V1-ndk.so
```

### Bibliotecas QCC 64-bit
```
system_ext/lib64/libqcc.so
system_ext/lib64/libqcc_file_agent_sys.so
system_ext/lib64/libqccdme.so
system_ext/lib64/libqccfileservice.so
system_ext/lib64/vendor.qti.hardware.qccsyshal@1.0.so
system_ext/lib64/vendor.qti.hardware.qccsyshal@1.1.so
system_ext/lib64/vendor.qti.hardware.qccsyshal@1.2-halimpl.so
system_ext/lib64/vendor.qti.hardware.qccsyshal@1.2.so
system_ext/lib64/vendor.qti.hardware.qccvndhal@1.0.so
system_ext/lib64/vendor.qti.qccsyshal_aidl-V1-ndk.so
system_ext/lib64/vendor.qti.qccsyshal_aidl-halimpl.so
system_ext/lib64/vendor.qti.qccvndhal_aidl-V1-ndk.so
```

### Digital Key Service
```
system_ext/priv-app/DckTimeSyncService
system_ext/priv-app/DckTimeSyncService/DckTimeSyncService.apk
```

---

## PRODUCT/ - 14 archivos

### Overlays Wi-Fi avanzados
```
product/overlay/SoftapOverlay6GHz
product/overlay/SoftapOverlay6GHz/SoftapOverlay6GHz.apk

product/overlay/SoftapOverlayDualAp
product/overlay/SoftapOverlayDualAp/SoftapOverlayDualAp.apk

product/overlay/SoftapOverlayOWE
product/overlay/SoftapOverlayOWE/SoftapOverlayOWE.apk
```

### UWB Overlay
```
product/overlay/UwbRROverlay.apk
```

### Overlay de dispositivo
```
product/overlay/framework-res__dm2qxxx__auto_generated_rro_product.apk
```

### Assistant Shell
```
product/app/AssistantShell
product/app/AssistantShell/AssistantShell.apk
```

---

## SYSTEM/ - Archivos CRÍTICOS (mínimo 11)

### Overlays de dispositivo (REQUERIDOS)
```
system/vendor/overlay/framework-res__dm2qxxx__auto_generated_rro_vendor.apk
system/vendor/overlay/framework-res__dm1qxxx__auto_generated_rro_vendor.apk
```

### Datos de cámara SM8550
```
system/cameradata/portrait_data/SRIB_Acenet_A16W8_V141_sm8550_snpe2704.dlc
system/cameradata/portrait_data/SRIB_DPD_A16W8_V013_sm8550_snpe2106.dlc
system/cameradata/portrait_data/SRIB_HDE_A16W8_V003_sm8550_snpe2433.dlc
system/cameradata/portrait_data/SRIB_Matting_INT8_V015_sm8550_snpe2108_TILE_896.dlc
system/cameradata/portrait_data/SRIB_SID_A16W8_V018_sm8550_snpe2433.dlc
```

### Configuración UWB
```
system/etc/libuwb-cal.conf
system/etc/init/init.system.uwb.rc
system/etc/init/digitalkey_init_uwb_tss2.rc
```

### Configuración dm2q
```
system/etc/init/ssu_dm2qxxx.rc
```

---

## SYSTEM/ - Bibliotecas CRÍTICAS (30 libs)

### Bibliotecas de seguridad (KeyMint V2 y AIDL)
```
system/lib/android.hardware.security.keymint-V2-ndk.so
system/lib64/android.hardware.security.keymint-V2-ndk.so
system/lib/vendor.samsung.hardware.keymint-V2-ndk.so
system/lib64/vendor.samsung.hardware.keymint-V2-ndk.so

system/lib/libsec_semAidl.so
system/lib64/libsec_semAidl.so
system/lib/libsec_skpmAidl.so
system/lib64/libsec_skpmAidl.so

system/lib/vendor.samsung.hardware.security.sem-V1-ndk.so
system/lib64/vendor.samsung.hardware.security.sem-V1-ndk.so
system/lib/vendor.samsung.hardware.security.skpm-V1-ndk.so
system/lib64/vendor.samsung.hardware.security.skpm-V1-ndk.so
```

### Bibliotecas de cámara y AI
```
system/lib64/libDocDeblur.camera.samsung.so
system/lib64/libDocObjectRemoval.camera.samsung.so
system/lib64/libDocObjectRemoval.enhanceX.samsung.so
system/lib64/libSceneDetector_v1.camera.samsung.so
system/lib64/libSemanticMap_v1.camera.samsung.so
system/lib/libSemanticMap_v1.camera.samsung.so
system/lib64/libSlowShutter-core.so
system/lib/libSlowShutter-core.so
system/lib64/libWideDistortionCorrection.camera.samsung.so

system/lib64/libacz_hhdr.arcsoft.so
system/lib64/libaiclearzoom_raw.arcsoft.so
system/lib64/libaiclearzoomraw_wrapper_v1.camera.samsung.so
system/lib64/libface_recognition.arcsoft.so
system/lib64/libpic_best.arcsoft.so
```

### Bibliotecas de media
```
system/lib64/libmediacaptureservice.so
system/lib64/libmediaplayerservice.so
system/lib64/libstagefright_httplive_sec.so
```

### Bibliotecas de audio
```
system/lib/libswdapaidl.so
system/lib64/libswdapaidl.so
system/lib/libswspatializeraidl.so
system/lib64/libswspatializeraidl.so
```

### Bibliotecas UWB
```
system/lib/libtflite_uwb_jni.so
system/lib64/libtflite_uwb_jni.so
```

### Bibliotecas FRC (Frame Rate Conversion)
```
system/lib/FrcMcWrapper.so
system/lib64/FrcMcWrapper.so
system/lib/libFrucPSVTLib.so
system/lib64/libFrucPSVTLib.so
system/lib/libaifrc.aidl.quram.so
system/lib64/libaifrc.aidl.quram.so
system/lib/libaifrcInterface.camera.samsung.so
system/lib64/libaifrcInterface.camera.samsung.so
system/lib/libmcaimegpu.samsung.so
system/lib64/libmcaimegpu.samsung.so
system/lib/vendor.samsung.hardware.frcmc-V1-ndk.so
system/lib64/vendor.samsung.hardware.frcmc-V1-ndk.so
```

---

## SYSTEM/ - Archivos OPCIONALES

### TTS Completo (si quieres soporte multiidioma) - ~150 archivos
```
system/app/SamsungTTS
system/app/SamsungTTS/SamsungTTS.apk

system/app/SamsungTTSVoice_ar_AE_m00
system/app/SamsungTTSVoice_ar_AE_m00/SamsungTTSVoice_ar_AE_m00.apk

system/app/SamsungTTSVoice_de_DE_f00
system/app/SamsungTTSVoice_de_DE_f00/SamsungTTSVoice_de_DE_f00.apk

system/app/SamsungTTSVoice_en_GB_f00
system/app/SamsungTTSVoice_en_GB_f00/SamsungTTSVoice_en_GB_f00.apk

system/app/SamsungTTSVoice_es_ES_f00
system/app/SamsungTTSVoice_es_ES_f00/SamsungTTSVoice_es_ES_f00.apk

system/app/SamsungTTSVoice_es_US_f00
system/app/SamsungTTSVoice_es_US_f00/SamsungTTSVoice_es_US_f00.apk

system/app/SamsungTTSVoice_fr_FR_f00
system/app/SamsungTTSVoice_fr_FR_f00/SamsungTTSVoice_fr_FR_f00.apk

system/app/SamsungTTSVoice_hi_IN_f00
system/app/SamsungTTSVoice_hi_IN_f00/SamsungTTSVoice_hi_IN_f00.apk

system/app/SamsungTTSVoice_id_ID_f00
system/app/SamsungTTSVoice_id_ID_f00/SamsungTTSVoice_id_ID_f00.apk

system/app/SamsungTTSVoice_it_IT_f00
system/app/SamsungTTSVoice_it_IT_f00/SamsungTTSVoice_it_IT_f00.apk

system/app/SamsungTTSVoice_pl_PL_f00
system/app/SamsungTTSVoice_pl_PL_f00/SamsungTTSVoice_pl_PL_f00.apk

system/app/SamsungTTSVoice_pt_BR_f00
system/app/SamsungTTSVoice_pt_BR_f00/SamsungTTSVoice_pt_BR_f00.apk

system/app/SamsungTTSVoice_ru_RU_f00
system/app/SamsungTTSVoice_ru_RU_f00/SamsungTTSVoice_ru_RU_f00.apk

system/app/SamsungTTSVoice_th_TH_f00
system/app/SamsungTTSVoice_th_TH_f00/SamsungTTSVoice_th_TH_f00.apk

system/app/SamsungTTSVoice_tr_TR_f00
system/app/SamsungTTSVoice_tr_TR_f00/SamsungTTSVoice_tr_TR_f00.apk

system/app/SamsungTTSVoice_vi_VN_f00
system/app/SamsungTTSVoice_vi_VN_f00/SamsungTTSVoice_vi_VN_f00.apk

system/app/SamsungTTSVoice_zh_CN_m00
system/app/SamsungTTSVoice_zh_CN_m00/SamsungTTSVoice_zh_CN_m00.apk
```
**Ver FILE_LISTS.md para la lista completa de archivos TTS**

### Apps adicionales
```
system/app/UwbTest
system/app/UwbTest/UwbTest.apk

system/app/SketchBook
system/app/SketchBook/SketchBook.apk
```

### Búsqueda de medios
```
system/etc/mediasearch/data/dec_adaptor.tflite
system/etc/mediasearch/data/dec_event.tflite
system/etc/mediasearch/data/enc_image.tflite
system/etc/mediasearch/data/enc_text.tflite
system/etc/mediasearch/data/versioninfo.json

system/etc/default-permissions/default-permissions-com.samsung.mediasearch.xml
system/etc/default-permissions/default-permissions-com.samsung.videoscan.xml
```

---

## RESUMEN DE ARCHIVOS A COPIAR

| Categoría | Archivos | Crítico |
|-----------|----------|---------|
| vendor/ | TODO | ✅ |
| Kernel/boot | 4 imgs | ✅ |
| Configs | 14 archivos | ✅ |
| system_ext/ | 41 archivos | ✅ |
| product/ | 14 archivos | ✅ |
| system/ críticos | 41 archivos | ✅ |
| system/ TTS | ~150 archivos | 🔶 |
| system/ apps | ~12 archivos | 🔶 |
| system/ media search | ~7 archivos | 🔶 |
| **TOTAL MÍNIMO** | **~10,125** | - |
| **TOTAL COMPLETO** | **~10,280+** | - |

