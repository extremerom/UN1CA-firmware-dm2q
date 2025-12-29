# Guía de Porteo: Adaptar Firmware r0q para dm2q

## ⚠️ ADVERTENCIA IMPORTANTE

**Este es un proceso complejo y arriesgado que puede dejar tu dispositivo inutilizable (brick). Solo usuarios avanzados con conocimientos de firmware Android deberían intentar esto.**

---

## Resumen Ejecutivo

### Archivos a COPIAR de dm2q → r0q

| Partición | Cantidad | Crítico | Descripción |
|-----------|----------|---------|-------------|
| **vendor/** | TODO | ✅ SÍ | Drivers de hardware completos |
| **boot/dtbo/vendor_boot** | 3 imgs | ✅ SÍ | Kernel y device tree |
| **system_ext/** | 41 archivos | ✅ SÍ | VNDK v33, QCC, Digital Key |
| **product/** | 14 archivos | ⚠️ Parcial | Wi-Fi 6E, UWB overlays |
| **system/** | 11-204 archivos | ⚠️ Parcial | Mínimo 11, máximo 204 |
| **Configs** | 14 archivos | ✅ SÍ | fs_config, file_context, dpolicy |

### Archivos a ELIMINAR de r0q

| Tipo | Cantidad | Razón |
|------|----------|-------|
| **VNDK v31** | 1 apex | Incompatible con Android 13 |
| **HALs antiguos** | ~20 libs | KeyMint v1→v2, HIDL→AIDL |
| **Cámara SM8450** | ~8 archivos | Incompatible con SM8550 |
| **Overlays r0q** | 2 apk | Identificación incorrecta |
| **Apps r0q** | 3-4 apps | Conflictos opcionales |

**Total archivos a modificar:** ~10,100+ (principalmente vendor/)

---

## Resumen del Problema

Quieres instalar el firmware de **r0q** (Android 12) en un dispositivo **dm2q** (Android 13), pero necesitas adaptarlo para que funcione correctamente con el hardware de dm2q.

**Problemas principales a resolver:**
- 🖼️ **Pantalla:** Drivers y configuración específicos del panel
- ⚡ **Carga rápida:** Controladores de batería y carga
- 🔊 **Audio:** HAL y configuración de audio
- 📡 **Conectividad:** Wi-Fi, Bluetooth, módem
- 📷 **Cámara:** Configuración y blobs específicos del hardware

---

## Estrategia de Porteo

### Opción Recomendada: Mantener Base r0q + Copiar Hardware dm2q

La mejor estrategia es:
1. Usar el firmware r0q como base (sistema, apps)
2. Reemplazar **SOLO** los componentes específicos de hardware de dm2q
3. Mantener la estructura de r0q pero con drivers de dm2q

---

## PASO 1: Archivos que DEBES COPIAR de dm2q a r0q

### A. Partición `vendor/` (COMPLETA)

**⚠️ CRÍTICO:** Copia **TODA** la partición `/vendor` de dm2q a r0q

```bash
# La partición vendor contiene TODOS los drivers específicos del hardware
vendor/
```

**¿Por qué?** La partición vendor contiene:
- Drivers de pantalla (display HAL)
- Drivers de audio
- Drivers de cámara
- Firmware de hardware (GPU, DSP, etc.)
- Controladores de carga
- Configuración de sensores
- Módulos del kernel específicos

### B. Kernel y Boot

**⚠️ CRÍTICO:** Usa el kernel de dm2q

```bash
# Archivos a copiar:
boot.img                    # Kernel completo de dm2q
dtbo.img                    # Device Tree Overlays
vendor_boot.img             # Ramdisk del vendor
```

### C. Archivos en system_ext/

**Copiar estos 41 archivos de dm2q a r0q:**

```bash
# VNDK (Android 13 vs 12)
system_ext/apex/com.android.vndk.v33.apex

# QCC (Qualcomm Car Connectivity) - 6 archivos principales
system_ext/app/QCC/
system_ext/bin/qccsyshal@1.2-service
system_ext/bin/qccsyshal_aidl-service
system_ext/etc/init/vendor.qti.hardware.qccsyshal@1.2-service.rc
system_ext/etc/init/vendor.qti.qccsyshal_aidl-service.rc
system_ext/etc/vintf/manifest/vendor.qti.qccsyshal_aidl-service.xml

# Bibliotecas QCC - 32-bit
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

# Bibliotecas QCC - 64-bit
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

# Digital Key Service
system_ext/priv-app/DckTimeSyncService/
system_ext/framework/org.carconnectivity.android.digitalkey.timesync.jar
```

### D. Archivos en product/

**Copiar estos 14 archivos de dm2q a r0q:**

```bash
# Wi-Fi 6E y características avanzadas
product/overlay/SoftapOverlay6GHz/
product/overlay/SoftapOverlayDualAp/
product/overlay/SoftapOverlayOWE/
product/overlay/UwbRROverlay.apk

# Overlay específico del dispositivo
product/overlay/framework-res__dm2qxxx__auto_generated_rro_product.apk

# Assistant Shell
product/app/AssistantShell/
```

### E. Archivos en system/ (Análisis Detallado)

**Total de archivos únicos en dm2q:** 204 archivos

#### E.1. Archivos CRÍTICOS para Hardware (DEBEN copiarse)

```bash
# Overlays de dispositivo (REQUERIDOS para identificación correcta)
system/vendor/overlay/framework-res__dm2qxxx__auto_generated_rro_vendor.apk
system/vendor/overlay/framework-res__dm1qxxx__auto_generated_rro_vendor.apk

# Datos de cámara para SM8550 (chip de dm2q vs SM8450 de r0q)
system/cameradata/portrait_data/SRIB_Acenet_A16W8_V141_sm8550_snpe2704.dlc
system/cameradata/portrait_data/SRIB_DPD_A16W8_V013_sm8550_snpe2106.dlc
system/cameradata/portrait_data/SRIB_HDE_A16W8_V003_sm8550_snpe2433.dlc
system/cameradata/portrait_data/SRIB_Matting_INT8_V015_sm8550_snpe2108_TILE_896.dlc
system/cameradata/portrait_data/SRIB_SID_A16W8_V018_sm8550_snpe2433.dlc

# Configuración UWB (Ultra-Wideband)
system/etc/libuwb-cal.conf
system/etc/init/init.system.uwb.rc
system/etc/init/digitalkey_init_uwb_tss2.rc

# Configuración específica de dm2q
system/etc/init/ssu_dm2qxxx.rc
```

**Nota sobre cámara:** dm2q usa **SM8550** (Snapdragon 8 Gen 2), mientras r0q usa **SM8450** (Snapdragon 8 Gen 1). Los archivos de cámara son diferentes.

#### E.2. Aplicaciones Específicas de dm2q

```bash
# UWB Test Tool (para probar Ultra-Wideband)
system/app/UwbTest/

# SketchBook (Aplicación de dibujo Samsung)
system/app/SketchBook/

# SamsungTTS completo con paquetes de voz (~150 archivos)
system/app/SamsungTTS/
system/app/SamsungTTSVoice_ar_AE_m00/
system/app/SamsungTTSVoice_de_DE_f00/
system/app/SamsungTTSVoice_en_GB_f00/
system/app/SamsungTTSVoice_es_ES_f00/
system/app/SamsungTTSVoice_es_US_f00/
system/app/SamsungTTSVoice_fr_FR_f00/
system/app/SamsungTTSVoice_hi_IN_f00/
system/app/SamsungTTSVoice_id_ID_f00/
system/app/SamsungTTSVoice_it_IT_f00/
system/app/SamsungTTSVoice_pl_PL_f00/
system/app/SamsungTTSVoice_ru_RU_f00/
system/app/SamsungTTSVoice_th_TH_f00/
system/app/SamsungTTSVoice_vi_VN_f00/
# ... más idiomas (ver FILE_LISTS.md para lista completa)
```

**Decisión sobre TTS:**
- **Opción 1 (Recomendada):** Copia solo `system/app/SamsungTTS/` sin los paquetes de voz → ~6 archivos
- **Opción 2:** Copia TTS completo con todos los idiomas → ~156 archivos (~200MB)
- **Opción 3:** Mantén `SamsungTTS_no_vdata` de r0q (más ligero pero sin voces)

#### E.3. Búsqueda de Medios

```bash
# Sistema de búsqueda de medios (fotos/videos)
system/etc/mediasearch/data/dec_adaptor.tflite
system/etc/mediasearch/data/dec_event.tflite
system/etc/mediasearch/data/enc_image.tflite
system/etc/mediasearch/data/enc_text.tflite
system/etc/mediasearch/data/versioninfo.json
system/etc/default-permissions/default-permissions-com.samsung.mediasearch.xml
system/etc/default-permissions/default-permissions-com.samsung.videoscan.xml
```

**¿Copiar?** OPCIONAL - Solo si quieres la función de búsqueda avanzada de medios

#### E.4. Archivos ÚNICOS a r0q (NO copiar, eliminar si existen)

```bash
# Herramientas específicas de r0q - ELIMINAR
system/app/Cameralyzer/                    # Herramienta de análisis de cámara
system/app/ClockPackage/                   # Reloj (puede causar conflictos)
system/app/MinusOnePage/                   # Widget de página principal
system/app/SamsungTTS_no_vdata/            # TTS sin datos (si copias el completo)

# Daemon de criptografía de r0q
system/bin/sdp_cryptod                     # MANTENER (no reemplazar)

# Datos de cámara para SM8450 - REEMPLAZAR con los de SM8550
system/cameradata/portrait_data/SRIB_Acenet_A16W8_V141_sm8450_snpe2108.dlc
system/cameradata/portrait_data/SRIB_Matting_INT8_V015_sm8450_snpe2108_TILE_896.dlc
system/cameradata/portrait_data/SRIB_SID_A16W8_V018_sm8450_snpe2106.dlc

# Configuración de digital key de r0q
system/etc/init/digitalkey_init_ble_tss2.rc  # Mantener si no tienes UWB
```

#### Resumen de Archivos system/

| Categoría | Acción | Cantidad |
|-----------|--------|----------|
| Overlays de dispositivo | ✅ COPIAR | 2 archivos |
| Datos de cámara SM8550 | ✅ COPIAR | 5 archivos |
| Configuración UWB | ✅ COPIAR | 3 archivos |
| Config específica dm2q | ✅ COPIAR | 1 archivo |
| TTS con voces | 🔶 OPCIONAL | ~156 archivos |
| UwbTest/SketchBook | 🔶 OPCIONAL | ~12 archivos |
| Búsqueda de medios | 🔶 OPCIONAL | ~7 archivos |
| **TOTAL MÍNIMO** | - | **11 archivos** |
| **TOTAL COMPLETO** | - | **204 archivos** |

### F. Configuración de Hardware

**Copiar archivos de configuración de dm2q:**

```bash
# Archivos fs_config
fs_config-system
fs_config-system_ext
fs_config-product
fs_config-vendor
fs_config-odm

# Contextos de seguridad
file_context-system
file_context-system_ext
file_context-product
file_context-vendor
file_context-odm

# Política DEFEX
system/dpolicy_system
```

---

## PASO 2: Archivos que DEBES ELIMINAR de r0q

### A. Eliminar VNDK antiguo

```bash
# Eliminar Android 12 VNDK (r0q) antes de instalar Android 13 VNDK (dm2q)
system_ext/apex/com.android.vndk.v31.apex
```

### B. Eliminar overlays específicos de r0q

```bash
# Eliminar overlays de r0q que causan conflictos de identificación
product/overlay/framework-res__r0qxxx__auto_generated_rro_product.apk
system/vendor/overlay/framework-res__r0qxxx__auto_generated_rro_vendor.apk
```

### C. Eliminar HALs y bibliotecas incompatibles de r0q

**⚠️ CRÍTICO:** Estos archivos de r0q usan versiones antiguas de APIs o HALs incompatibles con dm2q.

#### C.1. Bibliotecas de Seguridad (KeyMint v1 → v2)

```bash
# Eliminar versión V1 (r0q), se reemplaza con V2 (dm2q)
system/lib/android.hardware.security.keymint-V1-ndk.so
system/lib64/android.hardware.security.keymint-V1-ndk.so
system/lib/vendor.samsung.hardware.keymint-V1-ndk.so
system/lib64/vendor.samsung.hardware.keymint-V1-ndk.so

# Eliminar HALs antiguos de seguridad (HIDL → AIDL)
system/lib/libsec_semHal.so
system/lib64/libsec_semHal.so
system/lib/libsec_skpmHal.so
system/lib64/libsec_skpmHal.so
system/lib/vendor.samsung.hardware.security.sem@1.0.so
system/lib64/vendor.samsung.hardware.security.sem@1.0.so
system/lib/vendor.samsung.hardware.security.skpm@1.0.so
system/lib64/vendor.samsung.hardware.security.skpm@1.0.so
```

**Razón:** dm2q usa KeyMint V2 y AIDL en lugar de V1 y HIDL. Los HALs antiguos causan conflictos de autenticación y encriptación.

#### C.2. Bibliotecas de Cámara SM8450 (r0q)

```bash
# Eliminar datos de cámara para SM8450 (Snapdragon 8 Gen 1)
system/cameradata/portrait_data/SRIB_Acenet_A16W8_V141_sm8450_snpe2108.dlc
system/cameradata/portrait_data/SRIB_Matting_INT8_V015_sm8450_snpe2108_TILE_896.dlc
system/cameradata/portrait_data/SRIB_SID_A16W8_V018_sm8450_snpe2106.dlc

# Eliminar bibliotecas de procesamiento de cámara de r0q
system/lib64/libHREnhancementAPI.camera.samsung.so
system/lib64/libarcsoft_superresolution_bokeh.so
system/lib64/libhigh_dynamic_range.arcsoft.so
system/lib64/libhighres_enhancement.arcsoft.so
system/lib64/liblow_light_hdr.arcsoft.so
```

**Razón:** dm2q usa SM8550 (Snapdragon 8 Gen 2) con diferentes algoritmos de cámara. Los archivos de SM8450 causarán crashes de cámara.

#### C.3. Bibliotecas de Media y Servicios duplicados

```bash
# Eliminar si existen en system/ de r0q (dm2q los tiene diferentes)
system/lib/libmediacaptureservice.so
system/lib64/libmediacaptureservice.so
system/lib/libmediaplayerservice.so
system/lib64/libmediaplayerservice.so
system/lib/libstagefright_httplive_sec.so
system/lib64/libstagefright_httplive_sec.so
```

**Razón:** dm2q tiene versiones actualizadas de estos servicios para Android 13.

#### C.4. Bibliotecas de Dumpstate antiguas

```bash
# Eliminar HALs de dumpstate v1.x (r0q)
system/lib64/android.hardware.dumpstate@1.0.so
system/lib64/android.hardware.dumpstate@1.1.so
```

**Razón:** dm2q usa versiones más recientes integradas en el sistema.

#### C.5. Bibliotecas SDP (Sensitive Data Protection) antiguas

```bash
# MANTENER PERO NO COPIAR - dm2q no usa estas bibliotecas
# Si están en r0q, déjalas a menos que causen conflictos
system/lib/libsdp_crypto.so
system/lib64/libsdp_crypto.so
system/lib/libsdp_kekm.so
system/lib64/libsdp_kekm.so
system/lib/libsdp_sdk.so
system/lib64/libsdp_sdk.so
system/bin/sdp_cryptod
```

**Razón:** dm2q maneja SDP de forma diferente. Puede funcionar sin estas libs.

### D. Eliminar aplicaciones específicas de r0q (OPCIONAL)

```bash
# Herramientas de r0q que pueden causar conflictos
system/app/Cameralyzer/                    # Herramienta de análisis específica de r0q
system/app/ClockPackage/                   # Puede conflictuar con reloj de dm2q
system/app/MinusOnePage/                   # Widget específico de r0q

# TTS ligero de r0q (si instalas TTS completo de dm2q)
system/app/SamsungTTS_no_vdata/           # Versión sin voces
```

### E. Eliminar configuración de Digital Key BLE de r0q

```bash
# Si dm2q usa UWB, eliminar configuración BLE de r0q
system/etc/init/digitalkey_init_ble_tss2.rc
```

**Razón:** dm2q tiene `digitalkey_init_uwb_tss2.rc` para UWB. Ambos pueden conflictuar.

---

## PASO 3: Verificaciones Críticas

### Verificar Compatibilidad de Hardware

**✅ dm2q y r0q son COMPATIBLES porque ambos usan:**
- SoC: Qualcomm Snapdragon 8 Gen 1 (SM8450)
- Arquitectura: arm64-v8a
- Familia: Samsung Galaxy S22 series

**Diferencias clave:**
- dm2q: Galaxy S22 (modelo más reciente, más features)
- r0q: Galaxy S22 (modelo anterior o variante regional)

### Componentes que DEBEN coincidir

```bash
# Verifica estos archivos son de dm2q:
vendor/lib64/hw/android.hardware.graphics.mapper@4.0-impl-qti-display.so
vendor/lib64/hw/audio.primary.taro.so
vendor/lib64/hw/camera.qcom.so
vendor/lib/hw/power.qcom.so
vendor/firmware/
```

---

## PASO 4: Procedimiento de Instalación

### Preparación

1. **Haz backup completo** del dispositivo
2. **Desbloquea el bootloader** si no lo está
3. **Ten acceso a modo download/fastboot**
4. **Ten cable USB confiable** y batería al 100%

### Secuencia de Flash

```bash
# 1. Flash el kernel de dm2q PRIMERO
fastboot flash boot boot_dm2q.img
fastboot flash dtbo dtbo_dm2q.img
fastboot flash vendor_boot vendor_boot_dm2q.img

# 2. Flash partición vendor de dm2q (CRÍTICO)
fastboot flash vendor vendor_dm2q.img

# 3. Flash system modificado (r0q + archivos dm2q)
fastboot flash system system_modified.img

# 4. Flash system_ext modificado
fastboot flash system_ext system_ext_modified.img

# 5. Flash product modificado
fastboot flash product product_modified.img

# 6. Limpia datos de usuario
fastboot -w

# 7. Reinicia
fastboot reboot
```

---

## PASO 5: Problemas Comunes y Soluciones

### 🖼️ Problema: Pantalla negra o no enciende

**Causa:** Drivers de pantalla incorrectos

**Solución:**
- Verifica que `/vendor/lib64/hw/android.hardware.graphics.*` sean de dm2q
- Verifica que `dtbo.img` sea de dm2q
- Copia `/vendor/firmware/` completo de dm2q

### ⚡ Problema: Carga rápida no funciona

**Causa:** Controladores de batería/carga incorrectos

**Solución:**
- Verifica `/vendor/lib64/hw/power.qcom.so` es de dm2q
- Verifica `/vendor/etc/charging/` es de dm2q
- Verifica archivos en `/vendor/firmware/` relacionados con batería

### 🔊 Problema: Sin audio o audio distorsionado

**Causa:** HAL de audio incorrecto

**Solución:**
- Verifica `/vendor/lib64/hw/audio.primary.*.so` es de dm2q
- Copia `/vendor/etc/audio/` completo de dm2q
- Verifica `/vendor/lib64/libaudio*.so` son de dm2q

### 📡 Problema: Wi-Fi/Bluetooth no funciona

**Causa:** Firmware o drivers incorrectos

**Solución:**
- Verifica `/vendor/firmware/wlan/` es de dm2q
- Verifica `/vendor/firmware/` (archivos BT) son de dm2q
- Copia `/vendor/etc/wifi/` de dm2q

### 📷 Problema: Cámara no funciona o crashes

**Causa:** Blobs de cámara incorrectos

**Solución:**
- Verifica TODA la carpeta `/vendor/lib64/camera/` es de dm2q
- Verifica `/vendor/lib64/hw/camera.*.so` es de dm2q
- Copia `/system/cameradata/` de dm2q (si existe)

---

## Archivos Críticos por Función

### Para que funcione la PANTALLA:

```
vendor/lib64/hw/android.hardware.graphics.mapper@*.so
vendor/lib64/hw/android.hardware.graphics.composer@*.so
vendor/lib64/libsdmcore.so
vendor/lib64/libsdmutils.so
vendor/firmware/display/
dtbo.img (Device Tree)
```

### Para que funcione la CARGA RÁPIDA:

```
vendor/lib64/hw/power.qcom.so
vendor/lib64/libqti-perfd-client.so
vendor/etc/charging/
vendor/firmware/ (archivos de batería)
```

### Para que funcione el AUDIO:

```
vendor/lib64/hw/audio.primary.taro.so
vendor/lib64/libaudioroute.so
vendor/lib64/libacdb-fts.so
vendor/etc/audio/
vendor/firmware/ (archivos ADSP)
```

### Para que funcione MÓDEM/RIL:

```
vendor/lib64/libril-qc-*.so
vendor/lib64/libsec-ril*.so
vendor/etc/modem/
vendor/firmware/ (archivos de módem)
```

---

## Resumen de Archivos a Modificar

| Partición | Acción | Cantidad |
|-----------|--------|----------|
| **vendor/** | Copiar COMPLETA de dm2q | ~10,000+ archivos |
| **boot/dtbo/vendor_boot** | Copiar de dm2q | 3 imágenes |
| **system_ext/** | Copiar 41 archivos de dm2q | 41 archivos |
| **product/** | Copiar 14 archivos de dm2q | 14 archivos |
| **system/** | Copiar overlays + opcionales | 2-150 archivos |
| **fs_config** | Usar de dm2q | 7 archivos |
| **file_context** | Usar de dm2q | 7 archivos |
| **dpolicy_system** | Usar de dm2q | 1 archivo |

**Total estimado de cambios:** ~10,100+ archivos (principalmente vendor/)

---

## ⚠️ ADVERTENCIAS FINALES

1. **Este proceso puede dejar tu dispositivo inutilizable (brick)**
2. **Necesitas conocimientos avanzados de Android y herramientas de firmware**
3. **El firmware r0q es Android 12, dm2q es Android 13 - puede haber incompatibilidades**
4. **Algunos features de dm2q (Wi-Fi 6E, UWB) pueden no funcionar en hardware r0q**
5. **La garantía del dispositivo se pierde**
6. **Necesitas acceso a ambos firmwares completos (r0q y dm2q)**

---

## Alternativa Más Segura

**Recomendación:** En lugar de portar r0q a dm2q, considera:

1. **Usar el firmware oficial de dm2q** - Es más estable y seguro
2. **Modificar el firmware dm2q** - Agregar features de r0q que te gusten
3. **Crear una ROM personalizada** - Usar herramientas como LineageOS como base

---

## Herramientas Necesarias

- **Android Image Kitchen** - Para desempacar/empacar boot.img
- **simg2img / img2simg** - Para convertir imágenes sparse
- **lpunpack / lpmake** - Para trabajar con super.img (si aplica)
- **fastboot** - Para flashear particiones
- **adb** - Para debugging
- **Firmware completo de dm2q** - Todas las particiones
- **Firmware completo de r0q** - Todas las particiones

---

## Conclusión

El porteo es técnicamente posible porque dm2q y r0q comparten el mismo SoC, pero requiere:
- Reemplazar TODA la partición vendor de dm2q
- Usar el kernel de dm2q
- Copiar ~55 archivos específicos de system_ext/product
- Actualizar configuraciones de sistema

**Nivel de dificultad:** ⭐⭐⭐⭐⭐ (Muy Alto)

**Riesgo de brick:** ⚠️⚠️⚠️⚠️⚠️ (Muy Alto)

**Solo para usuarios muy experimentados con acceso a unbrick mediante JTAG o herramientas profesionales.**
