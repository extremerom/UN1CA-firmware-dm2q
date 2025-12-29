# Análisis de Archivos del Sistema - system/system

Este documento contiene listas separadas de archivos relacionados con componentes específicos del sistema encontrados en la carpeta `system/system`.

## Fecha de análisis
29 de diciembre de 2025

## Resumen
- **Pantalla (Display/Screen)**: 40 archivos
- **Carga Rápida (Fast Charging/Battery)**: 56 archivos
- **Vibración (Vibration/Haptic)**: 26 archivos
- **Audio (Audio/Sound)**: 236 archivos
- **Cámara (Camera)**: 203 archivos

---

## 1. PANTALLA (Display/Screen)

Archivos relacionados con pantalla, brillo, captura de pantalla y display remoto:

```
./app/BrightnessBackupService/BrightnessBackupService.apk
./app/BrightnessBackupService/oat/arm64/BrightnessBackupService.odex
./app/BrightnessBackupService/oat/arm64/BrightnessBackupService.vdex
./bin/blank_screen
./bin/remotedisplay
./bin/screencap
./bin/screenrecord
./etc/default_screenshot.png
./etc/init/blank_screen.rc
./etc/init/remotedisplay.rc
./etc/permissions/com.android.media.remotedisplay.xml
./etc/permissions/com.sec.feature.cocktailpanel.xml
./framework/com.android.media.remotedisplay.jar
./framework/displayaiqe_svc.jar
./framework/oat/arm/com.android.media.remotedisplay.odex
./framework/oat/arm/com.android.media.remotedisplay.vdex
./framework/oat/arm/displayaiqe_svc.odex
./framework/oat/arm/displayaiqe_svc.vdex
./framework/oat/arm64/com.android.media.remotedisplay.odex
./framework/oat/arm64/com.android.media.remotedisplay.vdex
./framework/oat/arm64/displayaiqe_svc.odex
./framework/oat/arm64/displayaiqe_svc.vdex
./lib/libnativedisplay.so
./lib/libremotedisplay.so
./lib64/libImageScreener.camera.samsung.so
./lib64/libgpu_display.dylib.so
./lib64/libnativedisplay.so
./lib64/libremotedisplay.so
./lib64/libremotedisplay_wfd.so
./lib64/libremotedisplayservice.so
./lib64/vendor.qti.hardware.display.composer3-V1-ndk.so
./lib64/vendor.samsung.hardware.security.hdcp.wifidisplay-V2-ndk.so
./media/audio/ui/Screen_Capture.ogg
./media/lcd_density.txt
./priv-app/DynamicLockscreen/DynamicLockscreen.apk
./priv-app/DynamicLockscreen/oat/arm64/DynamicLockscreen.odex
./priv-app/DynamicLockscreen/oat/arm64/DynamicLockscreen.vdex
./priv-app/TaskEdgePanel_v3.2/TaskEdgePanel_v3.2.apk
./priv-app/TaskEdgePanel_v3.2/oat/arm64/TaskEdgePanel_v3.2.odex
./priv-app/TaskEdgePanel_v3.2/oat/arm64/TaskEdgePanel_v3.2.vdex
```

**Total: 40 archivos**

---

## 2. CARGA RÁPIDA (Fast Charging/Battery/Power)

Archivos relacionados con carga rápida, batería y gestión de energía:

```
./bin/samsungpowersoundplay
./etc/init/init.sec-charger.rc
./etc/init/powersnd.rc
./etc/permissions/com.sec.feature.wirelesscharger_authentication.xml
./etc/res/images/charger/battery_fail.png
./etc/res/images/charger/battery_scale.png
./lib/android.hardware.power-V6-ndk.so
./lib/android.hardware.power.stats-V1-cpp.so
./lib/android.hardware.power.stats-V1-ndk.so
./lib/android.hardware.power.stats@1.0.so
./lib/android.hardware.power@1.0.so
./lib/android.hardware.power@1.1.so
./lib/android.hardware.power@1.2.so
./lib/android.hardware.power@1.3.so
./lib/libbattery.so
./lib/libbatterystats_aidl.so
./lib/libpower.so
./lib/libpowermanager.so
./lib/vendor.samsung.hardware.miscpower@2.0.so
./lib64/android.hardware.power-V6-ndk.so
./lib64/android.hardware.power.stats-V1-cpp.so
./lib64/android.hardware.power.stats-V1-ndk.so
./lib64/android.hardware.power.stats@1.0.so
./lib64/android.hardware.power@1.0.so
./lib64/android.hardware.power@1.1.so
./lib64/android.hardware.power@1.2.so
./lib64/android.hardware.power@1.3.so
./lib64/libbattery.so
./lib64/libbatterystats_aidl.so
./lib64/libpower.so
./lib64/libpower_monitor.dylib.so
./lib64/libpowermanager.so
./lib64/libsamsungpowersound.so
./lib64/vendor.samsung.hardware.miscpower@2.0.so
./media/audio/ui/ChargingStarted.ogg
./media/audio/ui/ChargingStarted_Calm.ogg
./media/audio/ui/ChargingStarted_Fast.ogg
./media/audio/ui/ChargingStarted_Fast_Calm.ogg
./media/audio/ui/ChargingStarted_Fast_Fun.ogg
./media/audio/ui/ChargingStarted_Fast_Retro.ogg
./media/audio/ui/ChargingStarted_Fun.ogg
./media/audio/ui/ChargingStarted_Retro.ogg
./media/audio/ui/LowBattery.ogg
./media/audio/ui/LowBattery_Calm.ogg
./media/audio/ui/LowBattery_Fun.ogg
./media/audio/ui/LowBattery_Retro.ogg
./media/audio/ui/TW_Battery_caution.ogg
./media/audio/ui/TW_Battery_swelling_warning.ogg
./media/audio/ui/WirelessChargingStarted.ogg
./media/battery_error.spi
./media/battery_low.spi
./media/battery_protection.spi
./media/battery_temperature_error.spi
./media/battery_temperature_limit.spi
./media/battery_water_usb.spi
./media/slow_charging_usb.spi
```

**Total: 56 archivos**

**Nota sobre Carga Rápida**: Los archivos con el prefijo "ChargingStarted_Fast" son específicos para la funcionalidad de carga rápida.

---

## 3. VIBRACIÓN (Vibration/Haptic)

Archivos relacionados con vibración y retroalimentación háptica:

```
./etc/vintf/manifest/manifest_services_android.frameworks.vibrator.xml
./lib/android.hardware.vibrator-V3-ndk.so
./lib/android.hardware.vibrator@1.0.so
./lib/android.hardware.vibrator@1.1.so
./lib/android.hardware.vibrator@1.2.so
./lib/android.hardware.vibrator@1.3.so
./lib/android.os.vibrator.flags-aconfig-cc.so
./lib/libvibrator.so
./lib/libvibratorservice.so
./lib/vendor.samsung.hardware.vibrator-V5-ndk.so
./lib/vendor.samsung.hardware.vibrator@2.0.so
./lib/vendor.samsung.hardware.vibrator@2.1.so
./lib/vendor.samsung.hardware.vibrator@2.2.so
./lib64/android.hardware.vibrator-V3-ndk.so
./lib64/android.hardware.vibrator@1.0.so
./lib64/android.hardware.vibrator@1.1.so
./lib64/android.hardware.vibrator@1.2.so
./lib64/android.hardware.vibrator@1.3.so
./lib64/android.os.vibrator.flags-aconfig-cc.so
./lib64/libvibrator.so
./lib64/libvibratorservice.so
./lib64/vendor.samsung.hardware.vibrator-V5-ndk.so
./lib64/vendor.samsung.hardware.vibrator@2.0.so
./lib64/vendor.samsung.hardware.vibrator@2.1.so
./lib64/vendor.samsung.hardware.vibrator@2.2.so
./media/audio/ui/VIB_Vibration_Call.ogg
```

**Total: 26 archivos**

---

## 4. AUDIO (Audio/Sound)

Archivos relacionados con audio, sonido, procesamiento de audio y codecs:

```
./app/AdaptSound_B
./app/AdaptSound_B/AdaptSound_B.apk
./app/AdaptSound_B/oat/arm64/AdaptSound_B.odex
./app/AdaptSound_B/oat/arm64/AdaptSound_B.vdex
./app/AudioMirroring
./app/AudioMirroring/AudioMirroring.apk
./app/AudioMirroring/oat/arm64/AudioMirroring.odex
./app/AudioMirroring/oat/arm64/AudioMirroring.vdex
./app/MediaProviderLegacy
./app/MediaProviderLegacy/MediaProviderLegacy.apk
./app/MediaProviderLegacy/oat/arm64/MediaProviderLegacy.odex
./app/MediaProviderLegacy/oat/arm64/MediaProviderLegacy.vdex
./app/MediaSearch
./app/MediaSearch/MediaSearch.apk
./app/MediaSearch/oat/arm64/MediaSearch.odex
./app/MediaSearch/oat/arm64/MediaSearch.vdex
./app/MultiSoundSetting
./app/MultiSoundSetting/MultiSoundSetting.apk
./app/MultiSoundSetting/oat/arm64/MultiSoundSetting.odex
./app/MultiSoundSetting/oat/arm64/MultiSoundSetting.vdex
./app/SecMediaProvider
./app/SecMediaProvider/SecMediaProvider.apk
./app/SecMediaProvider/oat/arm64/SecMediaProvider.odex
./app/SecMediaProvider/oat/arm64/SecMediaProvider.vdex
./app/SecSoundPicker
./app/SecSoundPicker/SecSoundPicker.apk
./app/SecSoundPicker/oat/arm64/SecSoundPicker.odex
./app/SecSoundPicker/oat/arm64/SecSoundPicker.vdex
./app/SoundAlive_B
./app/SoundAlive_B/SoundAlive_B.apk
./app/SoundAlive_B/oat/arm64/SoundAlive_B.odex
./app/SoundAlive_B/oat/arm64/SoundAlive_B.vdex
./bin/audioserver
./etc/audioserver.rc
./etc/init/audioserver.rc
./etc/media_codecs_performance_audio.xml
./etc/permissions/com.samsung.android.audiomirroring.xml
./lib/aaudio-aidl-cpp.so
./lib/aconfig_mediacodec_flags_c_lib.so
./lib/android.hardware.audio.common-V4-ndk.so
./lib/android.hardware.audio.common-util.so
./lib/android.hardware.audio.common@2.0.so
./lib/android.hardware.audio.common@4.0-util.so
./lib/android.hardware.audio.common@4.0.so
./lib/android.hardware.audio.common@5.0-util.so
./lib/android.hardware.audio.common@5.0.so
./lib/android.hardware.audio.common@6.0-util.so
./lib/android.hardware.audio.common@6.0.so
./lib/android.hardware.audio.core-V3-ndk.so
./lib/android.hardware.audio.core.sounddose-V3-ndk.so
./lib/android.hardware.audio.effect-V3-ndk.so
./lib/android.hardware.audio.effect@4.0.so
./lib/android.hardware.audio.effect@5.0.so
./lib/android.hardware.audio.effect@6.0-util.so
./lib/android.hardware.audio.effect@6.0.so
./lib/android.hardware.audio.sounddose-V3-ndk.so
./lib/android.hardware.audio@4.0.so
./lib/android.hardware.audio@5.0.so
./lib/android.hardware.audio@6.0-util.so
./lib/android.hardware.audio@6.0.so
./lib/android.media.audio-aconfig-cc.so
./lib/android.media.audio.common.types-V1-ndk.so
./lib/android.media.audio.common.types-V4-cpp.so
./lib/android.media.audio.common.types-V4-ndk.so
./lib/android.media.audio.eraser.types-V1-ndk.so
./lib/android.media.audiopolicy-aconfig-cc.so
./lib/audio-permission-aidl-cpp.so
./lib/audioclient-types-aidl-cpp.so
./lib/audioflinger-aidl-cpp.so
./lib/audiopolicy-aidl-cpp.so
./lib/audiopolicy-types-aidl-cpp.so
./lib/av-audio-types-aidl-ndk.so
./lib/com.android.media.aaudio-aconfig-cc.so
./lib/com.android.media.audio-aconfig-cc.so
./lib/com.android.media.audioclient-aconfig-cc.so
./lib/com.android.media.audioserver-aconfig-cc.so
./lib/libSlowShutter_jni.media.samsung.so
./lib/libSoundAlive_VSP_ver316c_ARMCpp.so
./lib/lib_SoundAlive_AlbumArt_ver105.so
./lib/lib_SoundAlive_SRC192_ver205a.so
./lib/lib_SoundAlive_SRC384_ver320.so
./lib/lib_SoundAlive_play_plus_ver800.so
./lib/lib_SoundBooster_ver1100.so
./lib/lib_soundaliveresampler.so
./lib/libaaudio.so
./lib/libaaudio_internal.so
./lib/libamDNN.media.samsung.so
./lib/libaudio-resampler.so
./lib/libaudio_aidl_conversion_common_cpp.so
./lib/libaudio_aidl_conversion_common_ndk.so
./lib/libaudio_aidl_conversion_common_ndk_cpp.so
./lib/libaudio_aidl_conversion_core_ndk.so
./lib/libaudio_aidl_conversion_effect_ndk.so
./lib/libaudioaidlcommon.so
./lib/libaudioclient.so
./lib/libaudioclient_aidl_conversion.so
./lib/libaudiocoreaaudiorecorder.so
./lib/libaudioeffect_jni.so
./lib/libaudiofoundation.so
./lib/libaudiohal.so
./lib/libaudiohal@6.0.so
./lib/libaudiohal@7.0.so
./lib/libaudiohal@7.1.so
./lib/libaudiohal@aidl.so
./lib/libaudiohal_deathhandler.so
./lib/libaudiomanager.so
./lib/libaudiomirroring.so
./lib/libaudiomirroring_jni.audiomirroring.samsung.so
./lib/libaudiopolicy.so
./lib/libaudiopolicycomponents.so
./lib/libaudiopolicyenginedefault.so
./lib/libaudiopolicymanagerdefault.so
./lib/libaudioprocessing.so
./lib/libaudiosaplus_sec_legacy.so
./lib/libaudiosolution_jni.so
./lib/libaudioutils.so
./lib/libcallaudio.so
./lib/libheifcapture_jni.media.samsung.so
./lib/libhiddensound.so
./lib/libjpegsq.media.samsung.so
./lib/libmedia.so
./lib/libmedia_codeclist.so
./lib/libmedia_codeclist_capabilities.so
./lib/libmedia_helper.so
./lib/libmedia_jni.so
./lib/libmedia_jni_utils.so
./lib/libmedia_omx.so
./lib/libmedia_omx_client.so
./lib/libmedia_quality_include.so
./lib/libmediacapture.so
./lib/libmediacapture_jni.so
./lib/libmediadrm.so
./lib/libmediadrmmetrics_consumer.so
./lib/libmediadrmmetrics_full.so
./lib/libmediadrmmetrics_lite.so
./lib/libmediametrics.so
./lib/libmediandk.so
./lib/libmediandk_utils.so
./lib/libmediaresourcehelper.so
./lib/libmediasndk.mediacore.samsung.so
./lib/libmediasndk.so
./lib/libmediautils.so
./lib/libmediautils_delayed.so
./lib/libsamsungSoundbooster_plus_legacy.so
./lib/libsecaudiocoreutils.so
./lib/libsecaudiohal.so
./lib/libsecaudiohal@1.0.so
./lib/libsecaudioinfo.so
./lib/libsecaudiomix.so
./lib/libsecaudiotestutils.so
./lib/libsemimagecrop_jni.media.samsung.so
./lib/libsemmediaplayer_jni.so
./lib/libsemmediapostprocessor_jni.so
./lib/libsimba.media.samsung.so
./lib/libsjpegxl.media.samsung.so
./lib/libslljpeg.media.samsung.so
./lib/libsoundextractor.so
./lib/libsoundpool.so
./lib/libstats_media_metrics.so
./lib/libsume_jni.media.samsung.so
./lib/libsume_mediabuffer_jni.media.samsung.so
./lib/media_quality_aidl_interface-cpp.so
./lib/mediametricsservice-aidl-cpp.so
./lib/vendor.samsung.hardware.audio@1.0.so
./lib/vendor.samsung.hardware.media.converter-V2-ndk.so
./lib/vendor.samsung.hardware.media.mpp-V5-ndk.so
./lib64/aaudio-aidl-cpp.so
./lib64/aconfig_mediacodec_flags_c_lib.so
./lib64/android.hardware.audio.common-V4-ndk.so
./lib64/android.hardware.audio.common-util.so
./lib64/android.hardware.audio.common@2.0.so
./lib64/android.hardware.audio.common@4.0-util.so
./lib64/android.hardware.audio.common@4.0.so
./lib64/android.hardware.audio.common@5.0-util.so
./lib64/android.hardware.audio.common@5.0.so
./lib64/android.hardware.audio.common@6.0-util.so
./lib64/android.hardware.audio.common@6.0.so
./lib64/android.hardware.audio.core-V3-ndk.so
./lib64/android.hardware.audio.core.sounddose-V3-ndk.so
./lib64/android.hardware.audio.effect-V3-ndk.so
./lib64/android.hardware.audio.effect@4.0.so
./lib64/android.hardware.audio.effect@5.0.so
./lib64/android.hardware.audio.effect@6.0-util.so
./lib64/android.hardware.audio.effect@6.0.so
./lib64/android.hardware.audio.sounddose-V3-ndk.so
./lib64/android.hardware.audio@4.0.so
./lib64/android.hardware.audio@5.0.so
./lib64/android.hardware.audio@6.0-util.so
./lib64/android.hardware.audio@6.0.so
./lib64/android.hardware.media.bufferpool2-V2-ndk.so
./lib64/android.hardware.media.bufferpool@2.0.so
./lib64/android.hardware.media.c2-V1-ndk.so
./lib64/android.hardware.media.c2@1.0.so
./lib64/android.hardware.media.c2@1.1.so
./lib64/android.hardware.media.c2@1.2.so
./lib64/android.hardware.media.omx@1.0.so
./lib64/android.hardware.media@1.0.so
./lib64/android.media.audio-aconfig-cc.so
./lib64/android.media.audio.common.types-V1-ndk.so
./lib64/android.media.audio.common.types-V4-cpp.so
./lib64/android.media.audio.common.types-V4-ndk.so
./lib64/android.media.audio.eraser.types-V1-ndk.so
./lib64/android.media.audiopolicy-aconfig-cc.so
./lib64/audio-permission-aidl-cpp.so
./lib64/audioclient-types-aidl-cpp.so
./lib64/audioflinger-aidl-cpp.so
./lib64/audiopolicy-aidl-cpp.so
./lib64/audiopolicy-types-aidl-cpp.so
./lib64/av-audio-types-aidl-ndk.so
./lib64/com.android.media.aaudio-aconfig-cc.so
./lib64/com.android.media.audio-aconfig-cc.so
./lib64/com.android.media.audioclient-aconfig-cc.so
./lib64/com.android.media.audioserver-aconfig-cc.so
./lib64/libAudioFWInterface.so
./lib64/libAudioTranscoder.so
./lib64/libSlowShutter_jni.media.samsung.so
./lib64/libSoundAlive_VSP_ver316c_ARMCpp.so
./lib64/lib_SoundAlive_AlbumArt_ver105.so
./lib64/lib_SoundAlive_SRC192_ver205a.so
./lib64/lib_SoundAlive_SRC384_ver320.so
./lib64/lib_SoundAlive_play_plus_ver800.so
./lib64/lib_SoundBooster_ver1100.so
./lib64/lib_soundaliveresampler.so
./lib64/libaaudio.so
./lib64/libaaudio_internal.so
./lib64/libaaudiorecorder.so
./lib64/libamDNN.media.samsung.so
./lib64/libandroid_audio.dylib.so
./lib64/libapex_motionphoto_utils_jni.media.samsung.so
./lib64/libaudio-resampler.so
./lib64/libaudio_aidl_conversion_common_cpp.so
./lib64/libaudio_aidl_conversion_common_ndk.so
./lib64/libaudio_aidl_conversion_common_ndk_cpp.so
./lib64/libaudio_aidl_conversion_core_ndk.so
./lib64/libaudio_aidl_conversion_effect_ndk.so
./lib64/libaudio_streams.dylib.so
./lib64/libaudio_util.dylib.so
./lib64/libaudioaidlcommon.so
./lib64/libaudioclient.so
./lib64/libaudioclient_aidl_conversion.so
./lib64/libaudiocoreaaudiorecorder.so
./lib64/libaudioeffect_jni.so
./lib64/libaudioflinger.so
./lib64/libaudioflinger_datapath.so
./lib64/libaudioflinger_fastpath.so
./lib64/libaudioflinger_timing.so
./lib64/libaudioflinger_utils.so
./lib64/libaudiofoundation.so
./lib64/libaudiohal.so
./lib64/libaudiohal@6.0.so
./lib64/libaudiohal@7.0.so
./lib64/libaudiohal@7.1.so
./lib64/libaudiohal@aidl.so
./lib64/libaudiohal_deathhandler.so
./lib64/libaudiomanager.so
./lib64/libaudiomirroring.so
./lib64/libaudiomirroring_jni.audiomirroring.samsung.so
./lib64/libaudiomirroringservice.so
./lib64/libaudiopermission.so
./lib64/libaudiopolicy.so
./lib64/libaudiopolicycomponents.so
./lib64/libaudiopolicyenginedefault.so
./lib64/libaudiopolicymanagerdefault.so
./lib64/libaudioprocessing.so
./lib64/libaudiosaplus_sec_legacy.so
./lib64/libaudiosolution_jni.so
./lib64/libaudiospdif.so
./lib64/libaudiotracer.so
./lib64/libaudiousecasevalidation.so
./lib64/libaudioutils.so
./lib64/libcallaudio.so
./lib64/libcontextanalyzer_jni.media.samsung.so
./lib64/libheifcapture_jni.media.samsung.so
./lib64/libhiddensound.so
./lib64/libhiddensoundclient.so
./lib64/libjpegsq.media.samsung.so
./lib64/libmedia.so
./lib64/libmedia_codeclist.so
./lib64/libmedia_codeclist_capabilities.so
./lib64/libmedia_helper.so
./lib64/libmedia_jni.so
./lib64/libmedia_jni_utils.so
./lib64/libmedia_omx.so
./lib64/libmedia_omx_client.so
./lib64/libmedia_quality_include.so
./lib64/libmediacapture.so
./lib64/libmediacapture_jni.so
./lib64/libmediacaptureservice.so
./lib64/libmediadrm.so
./lib64/libmediadrmmetrics_consumer.so
./lib64/libmediadrmmetrics_full.so
./lib64/libmediadrmmetrics_lite.so
./lib64/libmediaextractorservice.so
./lib64/libmediametrics.so
./lib64/libmediametricsservice.so
./lib64/libmediandk.so
./lib64/libmediandk_utils.so
./lib64/libmediaplayerservice.so
./lib64/libmediarelayengine.so
./lib64/libmediaresourcehelper.so
./lib64/libmediasndk.mediacore.samsung.so
./lib64/libmediasndk.so
./lib64/libmediautils.so
./lib64/libmediautils_delayed.so
./lib64/libmotionphoto_jni.media.samsung.so
./lib64/libmotionphoto_utils_jni.media.samsung.so
./lib64/libsamsungSoundbooster_plus_legacy.so
./lib64/libsamsungpowersound.so
./lib64/libsecaudiocoreutils.so
./lib64/libsecaudiohal.so
./lib64/libsecaudiohal@1.0.so
./lib64/libsecaudiohalproxy_system.so
./lib64/libsecaudioinfo.so
./lib64/libsecaudiomix.so
./lib64/libsecaudiomonomix.so
./lib64/libsecaudiotestutils.so
./lib64/libsemimagecrop_jni.media.samsung.so
./lib64/libsemmediaplayer_jni.so
./lib64/libsemmediapostprocessor_jni.so
./lib64/libsimba.media.samsung.so
./lib64/libsjpegxl.media.samsung.so
./lib64/libslljpeg.media.samsung.so
./lib64/libsounddose.so
./lib64/libsoundextractor.so
./lib64/libsoundpool.so
./lib64/libstats_media_metrics.so
./lib64/libsume_jni.media.samsung.so
./lib64/libsume_mediabuffer_jni.media.samsung.so
./lib64/libvirtio_media.dylib.so
./lib64/media_permission-aidl-cpp.so
./lib64/media_quality_aidl_interface-cpp.so
./lib64/mediametricsservice-aidl-cpp.so
./lib64/vendor.samsung.hardware.audio-V1-ndk.so
./lib64/vendor.samsung.hardware.audio@1.0.so
./lib64/vendor.samsung.hardware.media.converter-V2-ndk.so
./lib64/vendor.samsung.hardware.media.mpp-V5-ndk.so
./media/audio/ui/Media_preview_Over_the_horizon.ogg
```

**Total: 236 archivos**

**Nota**: Esta lista incluye bibliotecas de audio HAL (Hardware Abstraction Layer), codecs, servicios de audio, y aplicaciones relacionadas con el procesamiento de audio como SoundAlive y AdaptSound.

---

## 5. CÁMARA (Camera)

Archivos relacionados con la cámara, procesamiento de imagen y servicios de cámara:

```
./app/CameraExtensionsProxy/CameraExtensionsProxy.apk
./app/CameraExtensionsProxy/oat/arm64/CameraExtensionsProxy.odex
./app/CameraExtensionsProxy/oat/arm64/CameraExtensionsProxy.vdex
./app/FactoryCameraFB/FactoryCameraFB.apk
./app/FactoryCameraFB/oat/arm64/FactoryCameraFB.odex
./app/FactoryCameraFB/oat/arm64/FactoryCameraFB.vdex
./app/MoccaMobile/MoccaMobile.apk
./app/MoccaMobile/oat/arm64/MoccaMobile.odex
./app/MoccaMobile/oat/arm64/MoccaMobile.vdex
./app/VTCameraSetting/VTCameraSetting.apk
./app/VTCameraSetting/oat/arm64/VTCameraSetting.odex
./app/VTCameraSetting/oat/arm64/VTCameraSetting.vdex
./bin/cameraserver
./bin/virtual_camera
./cameradata/camera-feature.xml
./etc/default-permissions/default-permissions-com.samsung.android.vtcamerasettings.xml
./etc/init/cameraserver.rc
./etc/init/virtual_camera.hal.rc
./etc/permissions/cameraservice.xml
./etc/permissions/com.samsung.android.sdk.camera.processor.effect.xml
./etc/permissions/com.samsung.android.sdk.camera.processor.xml
./etc/permissions/com.sec.feature.cover.clearcameraviewcover.xml
./etc/permissions/privapp-permissions-com.sec.android.app.camera.xml
./etc/permissions/scamera_sdk_util.xml
./etc/permissions/scamera_sep.xml
./etc/permissions/sec_camerax_impl.xml
./etc/permissions/sec_camerax_service.xml
./etc/public.libraries-camera.samsung.txt
./etc/vintf/manifest/manifest_android.frameworks.cameraservice.service.xml
./framework/oat/arm/scamera_sdk_util.odex
./framework/oat/arm/scamera_sdk_util.vdex
./framework/oat/arm/scamera_sep.odex
./framework/oat/arm/scamera_sep.vdex
./framework/oat/arm/sec_camerax_impl.odex
./framework/oat/arm/sec_camerax_impl.vdex
./framework/oat/arm64/scamera_sdk_util.odex
./framework/oat/arm64/scamera_sdk_util.vdex
./framework/oat/arm64/scamera_sep.odex
./framework/oat/arm64/scamera_sep.vdex
./framework/oat/arm64/sec_camerax_impl.odex
./framework/oat/arm64/sec_camerax_impl.vdex
./framework/scamera_sdk_util.jar
./framework/scamera_sep.jar
./framework/sec_camerax_impl.jar
./lib/android.hardware.camera.common@1.0.so
./lib/android.hardware.camera.device@3.2.so
./lib/camera_platform_flags_c_lib.so
./lib/libFace_Landmark_API.camera.samsung.so
./lib/libInteractiveSegmentation.camera.samsung.so
./lib/libMattingCore.camera.samsung.so
./lib/libOpenCv.camera.samsung.so
./lib/libSegmentationCore.camera.samsung.so
./lib/libSemanticMap_v1.camera.samsung.so
./lib/libaifrcInterface.camera.samsung.so
./lib/libcamera2ndk.so
./lib/libcamera_client.so
./lib/libcamera_metadata.so
./lib/libcore2nativeutil.camera.samsung.so
./lib/libexifa.camera.samsung.so
./lib/libjpega.camera.samsung.so
./lib/libsec_camerax_util_jni.camera.samsung.so
./lib/libseccameracore2.so
./lib/libsecjpeginterface.camera.samsung.so
./lib64/android.hardware.camera.common-V1-ndk.so
./lib64/android.hardware.camera.common@1.0.so
./lib64/android.hardware.camera.device-V3-ndk.so
./lib64/android.hardware.camera.device@1.0.so
./lib64/android.hardware.camera.device@3.2.so
./lib64/android.hardware.camera.device@3.3.so
./lib64/android.hardware.camera.device@3.4.so
./lib64/android.hardware.camera.device@3.5.so
./lib64/android.hardware.camera.device@3.6.so
./lib64/android.hardware.camera.device@3.7.so
./lib64/android.hardware.camera.metadata-V3-ndk.so
./lib64/android.hardware.camera.metadata@3.2.so
./lib64/android.hardware.camera.metadata@3.3.so
./lib64/android.hardware.camera.metadata@3.4.so
./lib64/android.hardware.camera.metadata@3.5.so
./lib64/android.hardware.camera.metadata@3.6.so
./lib64/android.hardware.camera.provider-V3-ndk.so
./lib64/android.hardware.camera.provider@2.4.so
./lib64/android.hardware.camera.provider@2.5.so
./lib64/android.hardware.camera.provider@2.6.so
./lib64/camera_platform_flags_c_lib.so
./lib64/extractors/libsecamrextractor.so
./lib64/libAEBHDR_wrapper.camera.samsung.so
./lib64/libAIQSolution_MPI.camera.samsung.so
./lib64/libAIQSolution_MPISingleRGB40.camera.samsung.so
./lib64/libBeauty_v4.camera.samsung.so
./lib64/libBestPhoto.camera.samsung.so
./lib64/libC2paDps.camera.samsung.so
./lib64/libDLInterface_aidl.camera.samsung.so
./lib64/libDeepDocRectify.camera.samsung.so
./lib64/libDocDeblur.camera.samsung.so
./lib64/libDocObjectRemoval.camera.samsung.so
./lib64/libDocRectifyWrapper.camera.samsung.so
./lib64/libDualCamBokehCapture.camera.samsung.so
./lib64/libEventDetector.camera.samsung.so
./lib64/libFacePreProcessing_jni.camera.samsung.so
./lib64/libFaceRestoration.camera.samsung.so
./lib64/libFace_Landmark_API.camera.samsung.so
./lib64/libFace_Landmark_Engine.camera.samsung.so
./lib64/libFacialBasedSelfieCorrection.camera.samsung.so
./lib64/libFood.camera.samsung.so
./lib64/libFoodDetector.camera.samsung.so
./lib64/libHIDTSnapJNI.camera.samsung.so
./lib64/libHprFace_GAE_api.camera.samsung.so
./lib64/libHprFace_GAE_jni.camera.samsung.so
./lib64/libHpr_RecFace_dl_v1.0.camera.samsung.so
./lib64/libHpr_RecGAE_cvFeature_v1.0.camera.samsung.so
./lib64/libImageCropper.camera.samsung.so
./lib64/libImageScreener.camera.samsung.so
./lib64/libImageSegmenter_v1.camera.samsung.so
./lib64/libImageTagger.camera.samsung.so
./lib64/libInteractiveSegmentation.camera.samsung.so
./lib64/libLocalTM_pcc.camera.samsung.so
./lib64/libLttEngine.camera.samsung.so
./lib64/libMPISingleRGB40.camera.samsung.so
./lib64/libMPISingleRGB40Tuning.camera.samsung.so
./lib64/libMattingCore.camera.samsung.so
./lib64/libMultiFrameProcessing30.camera.samsung.so
./lib64/libMultiFrameProcessing30.snapwrapper.camera.samsung.so
./lib64/libMultiFrameProcessing30Tuning.camera.samsung.so
./lib64/libMyFilter.camera.samsung.so
./lib64/libMyFilterPlugin.camera.samsung.so
./lib64/libObjectDetector_v1.camera.samsung.so
./lib64/libOpenCv.camera.samsung.so
./lib64/libPetClustering.camera.samsung.so
./lib64/libPortraitSolution.camera.samsung.so
./lib64/libQREngine.camera.samsung.so
./lib64/libRectify.camera.samsung.so
./lib64/libRelighting_API.camera.samsung.so
./lib64/libRemasterEngine.camera.samsung.so
./lib64/libSceneDetector_v1.camera.samsung.so
./lib64/libSegmentationCore.camera.samsung.so
./lib64/libSemanticMap_v1.camera.samsung.so
./lib64/libSimpleDocRectify.camera.samsung.so
./lib64/libSmartScan.camera.samsung.so
./lib64/libStride.camera.samsung.so
./lib64/libStrideTensorflowLite.camera.samsung.so
./lib64/libSwIsp_core.camera.samsung.so
./lib64/libSwIsp_wrapper_v1.camera.samsung.so
./lib64/libUltraWideDistortionCorrection.camera.samsung.so
./lib64/libVideoClassifier.camera.samsung.so
./lib64/libWideDistortionCorrection.camera.samsung.so
./lib64/libaiclearzoomraw_wrapper_v1.camera.samsung.so
./lib64/libaifrcInterface.camera.samsung.so
./lib64/libarcsoft_dualcam_portraitlighting.so
./lib64/libarcsoft_single_cam_glasses_seg.so
./lib64/libcamera2ndk.so
./lib64/libcamera_client.so
./lib64/libcamera_metadata.so
./lib64/libcore2nativeutil.camera.samsung.so
./lib64/libdualcam_portraitlighting_gallery_360.so
./lib64/libdualcam_refocus_gallery_48.so
./lib64/libdualcam_refocus_gallery_54.so
./lib64/libdualcam_refocus_gallery_beyond.so
./lib64/libdualcam_refocus_gallery_front_beyond.so
./lib64/libdualcam_refocus_gallery_wt_beyond.so
./lib64/libdualcam_refocus_image.so
./lib64/libdvs.camera.samsung.so
./lib64/libexifa.camera.samsung.so
./lib64/libhumantracking_util.camera.samsung.so
./lib64/libhybridHDR_wrapper.camera.samsung.so
./lib64/libjpega.camera.samsung.so
./lib64/libmidas_DNNInterface.camera.samsung.so
./lib64/libmidas_core.camera.samsung.so
./lib64/libportrait_controller_engine.camera.samsung.so
./lib64/libportrait_controller_interface_jni.camera.samsung.so
./lib64/libsec_camerax_util_jni.camera.samsung.so
./lib64/libsecbufferhandler.camera.samsung.so
./lib64/libseccameracore2.so
./lib64/libsecimaging.camera.samsung.so
./lib64/libsecimaging_pdk.camera.samsung.so
./lib64/libsecjpeginterface.camera.samsung.so
./lib64/libsmart_cropping.camera.samsung.so
./lib64/libsrib_CNNInterface.camera.samsung.so
./lib64/libsrib_MQA.camera.samsung.so
./lib64/libsrib_humanaware_engine.camera.samsung.so
./lib64/libstartrail.camera.samsung.so
./lib64/libsuperresolutionraw_wrapper_v2.camera.samsung.so
./lib64/libsurfaceutil.camera.samsung.so
./lib64/libtensorflowLite.camera.samsung.so
./lib64/libtensorflowLite2_11_0_dynamic_camera.so
./lib64/libtensorflowlite_c.camera.samsung.so
./lib64/libtensorflowlite_inference_api.camera.samsung.so
./lib64/libtflite2.myfilters.camera.samsung.so
./lib64/vendor.samsung.hardware.camera.device-V1-ndk.so
./lib64/vendor.samsung.hardware.camera.device@5.0.so
./lib64/vendor.samsung.hardware.camera.provider-V1-ndk.so
./lib64/vendor.samsung.hardware.camera.provider@4.0.so
./media/audio/ui/Cam_Start.ogg
./media/audio/ui/Cam_Stop.ogg
./media/audio/ui/camera_click.ogg
./media/audio/ui/camera_focus.ogg
./priv-app/SCameraSDKService/SCameraSDKService.apk
./priv-app/SCameraSDKService/oat/arm64/SCameraSDKService.odex
./priv-app/SCameraSDKService/oat/arm64/SCameraSDKService.vdex
./priv-app/SamsungCamera/SamsungCamera.apk
./priv-app/SamsungCamera/SamsungCamera.apk.prof
./priv-app/SamsungCamera/oat/arm64/SamsungCamera.art
./priv-app/SamsungCamera/oat/arm64/SamsungCamera.odex
./priv-app/SamsungCamera/oat/arm64/SamsungCamera.vdex
./priv-app/sec_camerax_service/oat/arm64/sec_camerax_service.odex
./priv-app/sec_camerax_service/oat/arm64/sec_camerax_service.vdex
./priv-app/sec_camerax_service/sec_camerax_service.apk
```

**Total: 203 archivos**

**Nota**: Esta lista incluye bibliotecas avanzadas de procesamiento de imagen como detección facial, segmentación, corrección de distorsión, HDR, bokeh, filtros, y múltiples versiones del HAL de cámara.

---

## Observaciones Adicionales

### Arquitecturas Soportadas
El sistema soporta dos arquitecturas de procesador:
- **ARM (32-bit)**: Archivos en carpetas `lib/` y `oat/arm/`
- **ARM64 (64-bit)**: Archivos en carpetas `lib64/` y `oat/arm64/`

### Tipos de Archivos Principales
1. **Bibliotecas compartidas (.so)**: Implementaciones nativas de bajo nivel
2. **Aplicaciones (.apk)**: Aplicaciones Android preinstaladas
3. **Archivos compilados (.odex, .vdex, .oat, .art)**: Código optimizado para ART (Android Runtime)
4. **Frameworks (.jar)**: Bibliotecas Java del sistema
5. **Archivos de configuración (.xml, .rc, .txt)**: Permisos, manifiestos e inicialización
6. **Recursos multimedia (.ogg, .png, .spi)**: Sonidos, imágenes y animaciones del sistema

### Componentes de Hardware HAL (Hardware Abstraction Layer)
Todos los componentes principales (cámara, audio, display, vibrador, batería) tienen múltiples versiones de HAL para compatibilidad con diferentes versiones de Android y hardware específico de Samsung y Qualcomm.

### Samsung-Specific Components
El sistema incluye numerosas bibliotecas y servicios específicos de Samsung, identificables por el prefijo `samsung` o `sec` en los nombres de archivo, incluyendo:
- SoundAlive (procesamiento de audio Samsung)
- Tecnología de cámara Samsung avanzada (AI, segmentación, detección de escenas)
- Servicios de gestión de energía Samsung
- Display AI QE (Quality Enhancement)

---

## Generado automáticamente
Este documento fue generado mediante análisis del directorio `system/system` del firmware UN1CA para el dispositivo dm2q.
