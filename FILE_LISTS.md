# Listas Detalladas de Archivos: dm2q vs r0q

Este documento contiene las listas completas de archivos que son únicos a cada dispositivo o diferentes entre ellos.

## Formato de Archivo fs_config

Cada línea en los archivos fs_config tiene el formato:
```
ruta/archivo UID GID PERMISOS capabilities
```

Por ejemplo:
```
system/bin/app_process64 0 2000 755 capabilities=0x0
```

---

## 1. ARCHIVOS EN system/ ÚNICOS A dm2q (204 archivos)

system/app/SamsungTTS 0 0 755 capabilities=0x0
system/app/SamsungTTS/SamsungTTS.apk 0 0 644 capabilities=0x0
system/app/SamsungTTS/oat 0 0 755 capabilities=0x0
system/app/SamsungTTS/oat/arm64 0 0 755 capabilities=0x0
system/app/SamsungTTS/oat/arm64/SamsungTTS.odex 0 0 644 capabilities=0x0
system/app/SamsungTTS/oat/arm64/SamsungTTS.vdex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_ar_AE_m00 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_ar_AE_m00/SamsungTTSVoice_ar_AE_m00.apk 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_ar_AE_m00/oat 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_ar_AE_m00/oat/arm64 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_ar_AE_m00/oat/arm64/SamsungTTSVoice_ar_AE_m00.odex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_ar_AE_m00/oat/arm64/SamsungTTSVoice_ar_AE_m00.vdex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_de_DE_f00 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_de_DE_f00/SamsungTTSVoice_de_DE_f00.apk 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_de_DE_f00/oat 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_de_DE_f00/oat/arm64 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_de_DE_f00/oat/arm64/SamsungTTSVoice_de_DE_f00.odex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_de_DE_f00/oat/arm64/SamsungTTSVoice_de_DE_f00.vdex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_en_GB_f00 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_en_GB_f00/SamsungTTSVoice_en_GB_f00.apk 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_en_GB_f00/oat 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_en_GB_f00/oat/arm64 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_en_GB_f00/oat/arm64/SamsungTTSVoice_en_GB_f00.odex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_en_GB_f00/oat/arm64/SamsungTTSVoice_en_GB_f00.vdex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_es_ES_f00 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_es_ES_f00/SamsungTTSVoice_es_ES_f00.apk 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_es_ES_f00/oat 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_es_ES_f00/oat/arm64 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_es_ES_f00/oat/arm64/SamsungTTSVoice_es_ES_f00.odex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_es_ES_f00/oat/arm64/SamsungTTSVoice_es_ES_f00.vdex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_es_US_f00 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_es_US_f00/SamsungTTSVoice_es_US_f00.apk 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_es_US_f00/oat 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_es_US_f00/oat/arm64 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_es_US_f00/oat/arm64/SamsungTTSVoice_es_US_f00.odex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_es_US_f00/oat/arm64/SamsungTTSVoice_es_US_f00.vdex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_fr_FR_f00 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_fr_FR_f00/SamsungTTSVoice_fr_FR_f00.apk 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_fr_FR_f00/oat 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_fr_FR_f00/oat/arm64 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_fr_FR_f00/oat/arm64/SamsungTTSVoice_fr_FR_f00.odex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_fr_FR_f00/oat/arm64/SamsungTTSVoice_fr_FR_f00.vdex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_hi_IN_f00 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_hi_IN_f00/SamsungTTSVoice_hi_IN_f00.apk 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_hi_IN_f00/oat 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_hi_IN_f00/oat/arm64 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_hi_IN_f00/oat/arm64/SamsungTTSVoice_hi_IN_f00.odex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_hi_IN_f00/oat/arm64/SamsungTTSVoice_hi_IN_f00.vdex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_id_ID_f00 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_id_ID_f00/SamsungTTSVoice_id_ID_f00.apk 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_id_ID_f00/oat 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_id_ID_f00/oat/arm64 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_id_ID_f00/oat/arm64/SamsungTTSVoice_id_ID_f00.odex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_id_ID_f00/oat/arm64/SamsungTTSVoice_id_ID_f00.vdex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_it_IT_f00 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_it_IT_f00/SamsungTTSVoice_it_IT_f00.apk 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_it_IT_f00/oat 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_it_IT_f00/oat/arm64 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_it_IT_f00/oat/arm64/SamsungTTSVoice_it_IT_f00.odex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_it_IT_f00/oat/arm64/SamsungTTSVoice_it_IT_f00.vdex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_pl_PL_f00 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_pl_PL_f00/SamsungTTSVoice_pl_PL_f00.apk 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_pl_PL_f00/oat 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_pl_PL_f00/oat/arm64 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_pl_PL_f00/oat/arm64/SamsungTTSVoice_pl_PL_f00.odex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_pl_PL_f00/oat/arm64/SamsungTTSVoice_pl_PL_f00.vdex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_ru_RU_f00 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_ru_RU_f00/SamsungTTSVoice_ru_RU_f00.apk 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_ru_RU_f00/oat 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_ru_RU_f00/oat/arm64 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_ru_RU_f00/oat/arm64/SamsungTTSVoice_ru_RU_f00.odex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_ru_RU_f00/oat/arm64/SamsungTTSVoice_ru_RU_f00.vdex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_th_TH_f00 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_th_TH_f00/SamsungTTSVoice_th_TH_f00.apk 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_th_TH_f00/oat 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_th_TH_f00/oat/arm64 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_th_TH_f00/oat/arm64/SamsungTTSVoice_th_TH_f00.odex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_th_TH_f00/oat/arm64/SamsungTTSVoice_th_TH_f00.vdex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_vi_VN_f00 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_vi_VN_f00/SamsungTTSVoice_vi_VN_f00.apk 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_vi_VN_f00/oat 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_vi_VN_f00/oat/arm64 0 0 755 capabilities=0x0
system/app/SamsungTTSVoice_vi_VN_f00/oat/arm64/SamsungTTSVoice_vi_VN_f00.odex 0 0 644 capabilities=0x0
system/app/SamsungTTSVoice_vi_VN_f00/oat/arm64/SamsungTTSVoice_vi_VN_f00.vdex 0 0 644 capabilities=0x0
system/app/SketchBook 0 0 755 capabilities=0x0
system/app/SketchBook/SketchBook.apk 0 0 644 capabilities=0x0
system/app/SketchBook/oat 0 0 755 capabilities=0x0
system/app/SketchBook/oat/arm64 0 0 755 capabilities=0x0
system/app/SketchBook/oat/arm64/SketchBook.odex 0 0 644 capabilities=0x0
system/app/SketchBook/oat/arm64/SketchBook.vdex 0 0 644 capabilities=0x0
system/app/UwbTest 0 0 755 capabilities=0x0
system/app/UwbTest/UwbTest.apk 0 0 644 capabilities=0x0
system/app/UwbTest/oat 0 0 755 capabilities=0x0
system/app/UwbTest/oat/arm64 0 0 755 capabilities=0x0
system/app/UwbTest/oat/arm64/UwbTest.odex 0 0 644 capabilities=0x0
system/app/UwbTest/oat/arm64/UwbTest.vdex 0 0 644 capabilities=0x0
system/cameradata/portrait_data/SRIB_Acenet_A16W8_V141_sm8550_snpe2704.dlc 0 0 644 capabilities=0x0
system/cameradata/portrait_data/SRIB_DPD_A16W8_V013_sm8550_snpe2106.dlc 0 0 644 capabilities=0x0
system/cameradata/portrait_data/SRIB_HDE_A16W8_V003_sm8550_snpe2433.dlc 0 0 644 capabilities=0x0
system/cameradata/portrait_data/SRIB_Matting_INT8_V015_sm8550_snpe2108_TILE_896.dlc 0 0 644 capabilities=0x0
system/cameradata/portrait_data/SRIB_SID_A16W8_V018_sm8550_snpe2433.dlc 0 0 644 capabilities=0x0
system/etc/default-permissions/default-permissions-com.samsung.mediasearch.xml 0 0 644 capabilities=0x0
system/etc/default-permissions/default-permissions-com.samsung.videoscan.xml 0 0 644 capabilities=0x0
system/etc/init/digitalkey_init_uwb_tss2.rc 0 0 644 capabilities=0x0
system/etc/init/init.system.uwb.rc 0 0 644 capabilities=0x0
system/etc/init/ssu_dm2qxxx.rc 0 0 644 capabilities=0x0
system/etc/libuwb-cal.conf 0 0 644 capabilities=0x0
system/etc/mediasearch 0 0 755 capabilities=0x0
system/etc/mediasearch/data 0 0 755 capabilities=0x0
system/etc/mediasearch/data/dec_adaptor.tflite 0 0 644 capabilities=0x0
system/etc/mediasearch/data/dec_event.tflite 0 0 644 capabilities=0x0
system/etc/mediasearch/data/enc_image.tflite 0 0 644 capabilities=0x0
system/etc/mediasearch/data/enc_text.tflite 0 0 644 capabilities=0x0
system/etc/mediasearch/data/versioninfo.json 0 0 644 capabilities=0x0
system/etc/permissions/com.samsung.android.uwb_extras.xml 0 0 644 capabilities=0x0
system/etc/permissions/com.sec.feature.pocketsensitivitymode_level1.xml 0 0 644 capabilities=0x0
system/etc/permissions/org.carconnectivity.android.digitalkey.timesync.xml 0 0 644 capabilities=0x0
system/etc/permissions/privapp-permissions-com.samsung.android.dcktimesync.xml 0 0 644 capabilities=0x0
system/etc/permissions/privapp-permissions-com.samsung.mediasearch.xml 0 0 644 capabilities=0x0
system/etc/permissions/privapp-permissions-com.samsung.videoscan.xml 0 0 644 capabilities=0x0
system/etc/permissions/privapp-permissions-com.sec.android.app.uwbtest.xml 0 0 644 capabilities=0x0
system/etc/pp_model.tflite 0 0 644 capabilities=0x0
system/etc/saiv 0 0 755 capabilities=0x0
system/etc/saiv/image_understanding 0 0 755 capabilities=0x0
system/etc/saiv/image_understanding/db 0 0 755 capabilities=0x0
system/etc/saiv/image_understanding/db/aic_classifier 0 0 755 capabilities=0x0
system/etc/saiv/image_understanding/db/aic_classifier/aic_classifier_cnn.info 0 0 644 capabilities=0x0
system/etc/saiv/image_understanding/db/aic_detector 0 0 755 capabilities=0x0
system/etc/saiv/image_understanding/db/aic_detector/aic_detector_cnn.info 0 0 644 capabilities=0x0
system/framework/arm/boot-com.samsung.android.uwb_extras.art 0 0 644 capabilities=0x0
system/framework/arm/boot-com.samsung.android.uwb_extras.oat 0 0 644 capabilities=0x0
system/framework/arm/boot-com.samsung.android.uwb_extras.vdex 0 0 644 capabilities=0x0
system/framework/arm64/boot-com.samsung.android.uwb_extras.art 0 0 644 capabilities=0x0
system/framework/arm64/boot-com.samsung.android.uwb_extras.oat 0 0 644 capabilities=0x0
system/framework/arm64/boot-com.samsung.android.uwb_extras.vdex 0 0 644 capabilities=0x0
system/framework/boot-com.samsung.android.uwb_extras.vdex 0 0 644 capabilities=0x0
system/framework/com.samsung.android.uwb_extras.jar 0 0 644 capabilities=0x0
system/framework/oat/arm/semuwb-service.odex 0 0 644 capabilities=0x0
system/framework/oat/arm/semuwb-service.vdex 0 0 644 capabilities=0x0
system/framework/oat/arm64/semuwb-service.odex 0 0 644 capabilities=0x0
system/framework/oat/arm64/semuwb-service.vdex 0 0 644 capabilities=0x0
system/framework/semuwb-service.jar 0 0 644 capabilities=0x0
system/hidden/INTERNAL_SDCARD/Music/Samsung/Over_the_Horizon.m4a 0 0 644 capabilities=0x0
system/lib/FrcMcWrapper.so 0 0 644 capabilities=0x0
system/lib/android.hardware.security.keymint-V2-ndk.so 0 0 644 capabilities=0x0
system/lib/libFrucPSVTLib.so 0 0 644 capabilities=0x0
system/lib/libSemanticMap_v1.camera.samsung.so 0 0 644 capabilities=0x0
system/lib/libSlowShutter-core.so 0 0 644 capabilities=0x0
system/lib/libaifrc.aidl.quram.so 0 0 644 capabilities=0x0
system/lib/libaifrcInterface.camera.samsung.so 0 0 644 capabilities=0x0
system/lib/libmcaimegpu.samsung.so 0 0 644 capabilities=0x0
system/lib/libsec_semAidl.so 0 0 644 capabilities=0x0
system/lib/libsec_skpmAidl.so 0 0 644 capabilities=0x0
system/lib/libswdapaidl.so 0 0 644 capabilities=0x0
system/lib/libswspatializeraidl.so 0 0 644 capabilities=0x0
system/lib/libtflite_uwb_jni.so 0 0 644 capabilities=0x0
system/lib/vendor.samsung.hardware.frcmc-V1-ndk.so 0 0 644 capabilities=0x0
system/lib/vendor.samsung.hardware.keymint-V2-ndk.so 0 0 644 capabilities=0x0
system/lib/vendor.samsung.hardware.security.sem-V1-ndk.so 0 0 644 capabilities=0x0
system/lib/vendor.samsung.hardware.security.skpm-V1-ndk.so 0 0 644 capabilities=0x0
system/lib64/FrcMcWrapper.so 0 0 644 capabilities=0x0
system/lib64/android.hardware.security.keymint-V2-ndk.so 0 0 644 capabilities=0x0
system/lib64/libDocDeblur.camera.samsung.so 0 0 644 capabilities=0x0
system/lib64/libDocObjectRemoval.camera.samsung.so 0 0 644 capabilities=0x0
system/lib64/libDocObjectRemoval.enhanceX.samsung.so 0 0 644 capabilities=0x0
system/lib64/libFrucPSVTLib.so 0 0 644 capabilities=0x0
system/lib64/libSceneDetector_v1.camera.samsung.so 0 0 644 capabilities=0x0
system/lib64/libSemanticMap_v1.camera.samsung.so 0 0 644 capabilities=0x0
system/lib64/libSlowShutter-core.so 0 0 644 capabilities=0x0
system/lib64/libWideDistortionCorrection.camera.samsung.so 0 0 644 capabilities=0x0
system/lib64/libacz_hhdr.arcsoft.so 0 0 644 capabilities=0x0
system/lib64/libaiclearzoom_raw.arcsoft.so 0 0 644 capabilities=0x0
system/lib64/libaiclearzoomraw_wrapper_v1.camera.samsung.so 0 0 644 capabilities=0x0
system/lib64/libaifrc.aidl.quram.so 0 0 644 capabilities=0x0
system/lib64/libaifrcInterface.camera.samsung.so 0 0 644 capabilities=0x0
system/lib64/libface_recognition.arcsoft.so 0 0 644 capabilities=0x0
system/lib64/libmcaimegpu.samsung.so 0 0 644 capabilities=0x0
system/lib64/libmediacaptureservice.so 0 0 644 capabilities=0x0
system/lib64/libmediaplayerservice.so 0 0 644 capabilities=0x0
system/lib64/libpic_best.arcsoft.so 0 0 644 capabilities=0x0
system/lib64/libsec_semAidl.so 0 0 644 capabilities=0x0
system/lib64/libsec_skpmAidl.so 0 0 644 capabilities=0x0
system/lib64/libstagefright_httplive_sec.so 0 0 644 capabilities=0x0
system/lib64/libswdapaidl.so 0 0 644 capabilities=0x0
system/lib64/libswspatializeraidl.so 0 0 644 capabilities=0x0
system/lib64/libtflite_uwb_jni.so 0 0 644 capabilities=0x0
system/lib64/vendor.samsung.hardware.frcmc-V1-ndk.so 0 0 644 capabilities=0x0
system/lib64/vendor.samsung.hardware.keymint-V2-ndk.so 0 0 644 capabilities=0x0
system/lib64/vendor.samsung.hardware.security.sem-V1-ndk.so 0 0 644 capabilities=0x0
system/lib64/vendor.samsung.hardware.security.skpm-V1-ndk.so 0 0 644 capabilities=0x0
system/priv-app/GameDriver-SM8550 0 0 755 capabilities=0x0
system/priv-app/GameDriver-SM8550/GameDriver-SM8550.apk 0 0 644 capabilities=0x0
system/priv-app/MediaSearch 0 0 755 capabilities=0x0
system/priv-app/MediaSearch/MediaSearch.apk 0 0 644 capabilities=0x0
system/priv-app/MediaSearch/oat 0 0 755 capabilities=0x0
system/priv-app/MediaSearch/oat/arm64 0 0 755 capabilities=0x0
system/priv-app/MediaSearch/oat/arm64/MediaSearch.odex 0 0 644 capabilities=0x0
system/priv-app/MediaSearch/oat/arm64/MediaSearch.vdex 0 0 644 capabilities=0x0
system/priv-app/VideoScan 0 0 755 capabilities=0x0
system/priv-app/VideoScan/VideoScan.apk 0 0 644 capabilities=0x0
system/priv-app/VideoScan/oat 0 0 755 capabilities=0x0
system/priv-app/VideoScan/oat/arm64 0 0 755 capabilities=0x0
system/priv-app/VideoScan/oat/arm64/VideoScan.odex 0 0 644 capabilities=0x0
system/priv-app/VideoScan/oat/arm64/VideoScan.vdex 0 0 644 capabilities=0x0

---

## 2. ARCHIVOS EN system/ ÚNICOS A r0q (87 archivos)

system/app/Cameralyzer 0 0 755 capabilities=0x0
system/app/Cameralyzer/Cameralyzer.apk 0 0 644 capabilities=0x0
system/app/Cameralyzer/oat 0 0 755 capabilities=0x0
system/app/Cameralyzer/oat/arm64 0 0 755 capabilities=0x0
system/app/Cameralyzer/oat/arm64/Cameralyzer.odex 0 0 644 capabilities=0x0
system/app/Cameralyzer/oat/arm64/Cameralyzer.vdex 0 0 644 capabilities=0x0
system/app/ClockPackage 0 0 755 capabilities=0x0
system/app/ClockPackage/ClockPackage.apk 0 0 644 capabilities=0x0
system/app/ClockPackage/oat 0 0 755 capabilities=0x0
system/app/ClockPackage/oat/arm64 0 0 755 capabilities=0x0
system/app/ClockPackage/oat/arm64/ClockPackage.odex 0 0 644 capabilities=0x0
system/app/ClockPackage/oat/arm64/ClockPackage.vdex 0 0 644 capabilities=0x0
system/app/MinusOnePage 0 0 755 capabilities=0x0
system/app/MinusOnePage/MinusOnePage.apk 0 0 644 capabilities=0x0
system/app/MinusOnePage/oat 0 0 755 capabilities=0x0
system/app/MinusOnePage/oat/arm64 0 0 755 capabilities=0x0
system/app/MinusOnePage/oat/arm64/MinusOnePage.odex 0 0 644 capabilities=0x0
system/app/MinusOnePage/oat/arm64/MinusOnePage.vdex 0 0 644 capabilities=0x0
system/app/SamsungTTS_no_vdata 0 0 755 capabilities=0x0
system/app/SamsungTTS_no_vdata/SamsungTTS_no_vdata.apk 0 0 644 capabilities=0x0
system/app/SamsungTTS_no_vdata/oat 0 0 755 capabilities=0x0
system/app/SamsungTTS_no_vdata/oat/arm64 0 0 755 capabilities=0x0
system/app/SamsungTTS_no_vdata/oat/arm64/SamsungTTS_no_vdata.odex 0 0 644 capabilities=0x0
system/app/SamsungTTS_no_vdata/oat/arm64/SamsungTTS_no_vdata.vdex 0 0 644 capabilities=0x0
system/bin/sdp_cryptod 0 2000 755 capabilities=0x0
system/cameradata/portrait_data/SRIB_Acenet_A16W8_V141_sm8450_snpe2108.dlc 0 0 644 capabilities=0x0
system/cameradata/portrait_data/SRIB_Matting_INT8_V015_sm8450_snpe2108_TILE_896.dlc 0 0 644 capabilities=0x0
system/cameradata/portrait_data/SRIB_SID_A16W8_V018_sm8450_snpe2106.dlc 0 0 644 capabilities=0x0
system/etc/default-permissions/default-permissions-com.sec.factory.cameralyzer.xml 0 0 644 capabilities=0x0
system/etc/init/digitalkey_init_ble_tss2.rc 0 0 644 capabilities=0x0
system/etc/init/rscmgr.rc 0 0 644 capabilities=0x0
system/etc/init/sdp_cryptod.rc 0 0 644 capabilities=0x0
system/etc/init/ssu_r0qxxx.rc 0 0 644 capabilities=0x0
system/etc/permissions/com.sec.feature.cover.ledbackcover.xml 0 0 644 capabilities=0x0
system/etc/permissions/com.sec.feature.cover.nfcledcover.xml 0 0 644 capabilities=0x0
system/etc/permissions/com.sec.feature.pocketmode_level33.xml 0 0 644 capabilities=0x0
system/etc/permissions/privapp-permissions-com.samsung.unifiedtp.xml 0 0 644 capabilities=0x0
system/etc/permissions/privapp-permissions-com.sec.android.cover.ledcover.xml 0 0 644 capabilities=0x0
system/hidden/INTERNAL_SDCARD/Music/Samsung/Over_the_Horizon.mp3 0 0 644 capabilities=0x0
system/lib/android.hardware.security.keymint-V1-ndk.so 0 0 644 capabilities=0x0
system/lib/libmdfpp_req.so 0 0 644 capabilities=0x0
system/lib/libmediacaptureservice.so 0 0 644 capabilities=0x0
system/lib/libmediaplayerservice.so 0 0 644 capabilities=0x0
system/lib/libsdp_crypto.so 0 0 644 capabilities=0x0
system/lib/libsdp_kekm.so 0 0 644 capabilities=0x0
system/lib/libsdp_sdk.so 0 0 644 capabilities=0x0
system/lib/libsec_semHal.so 0 0 644 capabilities=0x0
system/lib/libsec_skpmHal.so 0 0 644 capabilities=0x0
system/lib/libstagefright_httplive_sec.so 0 0 644 capabilities=0x0
system/lib/vendor.samsung.hardware.keymint-V1-ndk.so 0 0 644 capabilities=0x0
system/lib/vendor.samsung.hardware.security.sem@1.0.so 0 0 644 capabilities=0x0
system/lib/vendor.samsung.hardware.security.skpm@1.0.so 0 0 644 capabilities=0x0
system/lib64/android.hardware.dumpstate@1.0.so 0 0 644 capabilities=0x0
system/lib64/android.hardware.dumpstate@1.1.so 0 0 644 capabilities=0x0
system/lib64/android.hardware.security.keymint-V1-ndk.so 0 0 644 capabilities=0x0
system/lib64/libHREnhancementAPI.camera.samsung.so 0 0 644 capabilities=0x0
system/lib64/libarcsoft_superresolution_bokeh.so 0 0 644 capabilities=0x0
system/lib64/libhigh_dynamic_range.arcsoft.so 0 0 644 capabilities=0x0
system/lib64/libhighres_enhancement.arcsoft.so 0 0 644 capabilities=0x0
system/lib64/liblow_light_hdr.arcsoft.so 0 0 644 capabilities=0x0
system/lib64/libmdfpp_req.so 0 0 644 capabilities=0x0
system/lib64/libsdp_crypto.so 0 0 644 capabilities=0x0
system/lib64/libsdp_kekm.so 0 0 644 capabilities=0x0
system/lib64/libsdp_sdk.so 0 0 644 capabilities=0x0
system/lib64/libsec_semHal.so 0 0 644 capabilities=0x0
system/lib64/libsec_skpmHal.so 0 0 644 capabilities=0x0
system/lib64/vendor.samsung.hardware.keymint-V1-ndk.so 0 0 644 capabilities=0x0
system/lib64/vendor.samsung.hardware.security.sem@1.0.so 0 0 644 capabilities=0x0
system/lib64/vendor.samsung.hardware.security.skpm@1.0.so 0 0 644 capabilities=0x0
system/priv-app/GameDriver-SM8450 0 0 755 capabilities=0x0
system/priv-app/GameDriver-SM8450/GameDriver-SM8450.apk 0 0 644 capabilities=0x0
system/priv-app/LedCoverService 0 0 755 capabilities=0x0
system/priv-app/LedCoverService/LedCoverService.apk 0 0 644 capabilities=0x0
system/priv-app/LedCoverService/oat 0 0 755 capabilities=0x0
system/priv-app/LedCoverService/oat/arm64 0 0 755 capabilities=0x0
system/priv-app/LedCoverService/oat/arm64/LedCoverService.odex 0 0 644 capabilities=0x0
system/priv-app/LedCoverService/oat/arm64/LedCoverService.vdex 0 0 644 capabilities=0x0
system/priv-app/SVoiceIME 0 0 755 capabilities=0x0
system/priv-app/SVoiceIME/SVoiceIME.apk 0 0 644 capabilities=0x0
system/priv-app/UnifiedTetheringProvision 0 0 755 capabilities=0x0
system/priv-app/UnifiedTetheringProvision/UnifiedTetheringProvision.apk 0 0 644 capabilities=0x0
system/priv-app/UnifiedTetheringProvision/oat 0 0 755 capabilities=0x0
system/priv-app/UnifiedTetheringProvision/oat/arm64 0 0 755 capabilities=0x0
system/priv-app/UnifiedTetheringProvision/oat/arm64/UnifiedTetheringProvision.odex 0 0 644 capabilities=0x0
system/priv-app/UnifiedTetheringProvision/oat/arm64/UnifiedTetheringProvision.vdex 0 0 644 capabilities=0x0
system/saiv/localtm/pcc_front_photo_flashoff.dat 0 0 644 capabilities=0x0
system/saiv/localtm/pcc_front_photo_flashon.dat 0 0 644 capabilities=0x0

---

## 3. ARCHIVOS EN system_ext/ ÚNICOS A dm2q (41 archivos)

system_ext/apex/com.android.vndk.v33.apex 0 0 644 capabilities=0x0
system_ext/app/QCC 0 0 755 capabilities=0x0
system_ext/app/QCC/QCC.apk 0 0 644 capabilities=0x0
system_ext/app/QCC/oat 0 0 755 capabilities=0x0
system_ext/app/QCC/oat/arm64 0 0 755 capabilities=0x0
system_ext/app/QCC/oat/arm64/QCC.odex 0 0 644 capabilities=0x0
system_ext/app/QCC/oat/arm64/QCC.vdex 0 0 644 capabilities=0x0
system_ext/bin/qccsyshal@1.2-service 0 2000 755 capabilities=0x0
system_ext/bin/qccsyshal_aidl-service 0 2000 755 capabilities=0x0
system_ext/etc/init/vendor.qti.hardware.qccsyshal@1.2-service.rc 0 0 644 capabilities=0x0
system_ext/etc/init/vendor.qti.qccsyshal_aidl-service.rc 0 0 644 capabilities=0x0
system_ext/etc/vintf/manifest/vendor.qti.qccsyshal_aidl-service.xml 0 0 644 capabilities=0x0
system_ext/framework/org.carconnectivity.android.digitalkey.timesync.jar 0 0 644 capabilities=0x0
system_ext/lib/libqcc.so 0 0 644 capabilities=0x0
system_ext/lib/libqcc_file_agent_sys.so 0 0 644 capabilities=0x0
system_ext/lib/libqccdme.so 0 0 644 capabilities=0x0
system_ext/lib/libqccfileservice.so 0 0 644 capabilities=0x0
system_ext/lib/vendor.qti.hardware.qccsyshal@1.0.so 0 0 644 capabilities=0x0
system_ext/lib/vendor.qti.hardware.qccsyshal@1.1.so 0 0 644 capabilities=0x0
system_ext/lib/vendor.qti.hardware.qccsyshal@1.2.so 0 0 644 capabilities=0x0
system_ext/lib/vendor.qti.hardware.qccvndhal@1.0.so 0 0 644 capabilities=0x0
system_ext/lib/vendor.qti.qccsyshal_aidl-V1-ndk.so 0 0 644 capabilities=0x0
system_ext/lib/vendor.qti.qccvndhal_aidl-V1-ndk.so 0 0 644 capabilities=0x0
system_ext/lib64/libqcc.so 0 0 644 capabilities=0x0
system_ext/lib64/libqcc_file_agent_sys.so 0 0 644 capabilities=0x0
system_ext/lib64/libqccdme.so 0 0 644 capabilities=0x0
system_ext/lib64/libqccfileservice.so 0 0 644 capabilities=0x0
system_ext/lib64/vendor.qti.hardware.qccsyshal@1.0.so 0 0 644 capabilities=0x0
system_ext/lib64/vendor.qti.hardware.qccsyshal@1.1.so 0 0 644 capabilities=0x0
system_ext/lib64/vendor.qti.hardware.qccsyshal@1.2-halimpl.so 0 0 644 capabilities=0x0
system_ext/lib64/vendor.qti.hardware.qccsyshal@1.2.so 0 0 644 capabilities=0x0
system_ext/lib64/vendor.qti.hardware.qccvndhal@1.0.so 0 0 644 capabilities=0x0
system_ext/lib64/vendor.qti.qccsyshal_aidl-V1-ndk.so 0 0 644 capabilities=0x0
system_ext/lib64/vendor.qti.qccsyshal_aidl-halimpl.so 0 0 644 capabilities=0x0
system_ext/lib64/vendor.qti.qccvndhal_aidl-V1-ndk.so 0 0 644 capabilities=0x0
system_ext/priv-app/DckTimeSyncService 0 0 755 capabilities=0x0
system_ext/priv-app/DckTimeSyncService/DckTimeSyncService.apk 0 0 644 capabilities=0x0
system_ext/priv-app/DckTimeSyncService/oat 0 0 755 capabilities=0x0
system_ext/priv-app/DckTimeSyncService/oat/arm64 0 0 755 capabilities=0x0
system_ext/priv-app/DckTimeSyncService/oat/arm64/DckTimeSyncService.odex 0 0 644 capabilities=0x0
system_ext/priv-app/DckTimeSyncService/oat/arm64/DckTimeSyncService.vdex 0 0 644 capabilities=0x0

---

## 4. ARCHIVOS EN system_ext/ ÚNICOS A r0q (1 archivo)

system_ext/apex/com.android.vndk.v31.apex 0 0 644 capabilities=0x0

---

## 5. ARCHIVOS EN product/ ÚNICOS A dm2q (14 archivos)

product/app/AssistantShell 0 0 755 capabilities=0x0
product/app/AssistantShell/AssistantShell.apk 0 0 644 capabilities=0x0
product/app/AssistantShell/oat 0 0 755 capabilities=0x0
product/app/AssistantShell/oat/arm64 0 0 755 capabilities=0x0
product/app/AssistantShell/oat/arm64/AssistantShell.odex 0 0 644 capabilities=0x0
product/app/AssistantShell/oat/arm64/AssistantShell.vdex 0 0 644 capabilities=0x0
product/overlay/SoftapOverlay6GHz 0 0 755 capabilities=0x0
product/overlay/SoftapOverlay6GHz/SoftapOverlay6GHz.apk 0 0 644 capabilities=0x0
product/overlay/SoftapOverlayDualAp 0 0 755 capabilities=0x0
product/overlay/SoftapOverlayDualAp/SoftapOverlayDualAp.apk 0 0 644 capabilities=0x0
product/overlay/SoftapOverlayOWE 0 0 755 capabilities=0x0
product/overlay/SoftapOverlayOWE/SoftapOverlayOWE.apk 0 0 644 capabilities=0x0
product/overlay/UwbRROverlay.apk 0 0 644 capabilities=0x0
product/overlay/framework-res__dm2qxxx__auto_generated_rro_product.apk 0 0 644 capabilities=0x0

---

## 6. ARCHIVOS EN product/ ÚNICOS A r0q (1 archivo)

product/overlay/framework-res__r0qxxx__auto_generated_rro_product.apk 0 0 644 capabilities=0x0
