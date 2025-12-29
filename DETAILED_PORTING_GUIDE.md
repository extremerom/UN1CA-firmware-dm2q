# Guía Detallada de Porteo: r0q → dm2q

## Introducción

Esta guía te ayuda a adaptar el firmware de **r0q** (Android 12) para que funcione en hardware **dm2q** (Android 13).

**⚠️ IMPORTANTE:**
- Ya tienes la partición vendor/ de dm2q instalada ✅
- Esta guía cubre SOLO: system/, system_ext/ y product/
- Total de cambios necesarios: ~280 archivos

---

## Estrategia General

```
Base: Firmware r0q
  ↓
Eliminar: 87 archivos de r0q incompatibles
  ↓
Agregar: 259 archivos de dm2q
  ↓
Resultado: Firmware híbrido funcional para dm2q
```

---

# PARTE 1: PARTICIÓN system_ext/

## Análisis system_ext/

**Estado actual:**
- r0q: 1096 archivos (Android 12, VNDK 31)
- dm2q: 1136 archivos (Android 13, VNDK 33)
- Comunes: 1095 archivos (99.9%)

## 1.1 Archivos a ELIMINAR de system_ext/ (1 archivo)

```bash
# Android 12 VNDK (INCOMPATIBLE con Android 13)
rm system_ext/apex/com.android.vndk.v31.apex
```

## 1.2 Archivos a COPIAR de dm2q a system_ext/ (41 archivos)

### A. VNDK Android 13 (CRÍTICO)
```bash
system_ext/apex/com.android.vndk.v33.apex
```
**Función:** Biblioteca de compatibilidad vendor/system para Android 13

---

### B. QCC - Qualcomm Car Connectivity (26 archivos)

**¿Qué es QCC?**
- Suite de conectividad vehicular de Qualcomm
- Permite Android Auto mejorado
- Integración con sistemas del automóvil

#### Aplicación Principal
```bash
system_ext/app/QCC
system_ext/app/QCC/QCC.apk
```

#### Servicios QCC
```bash
system_ext/bin/qccsyshal@1.2-service
system_ext/bin/qccsyshal_aidl-service
```

#### Configuración de Servicios
```bash
system_ext/etc/init/vendor.qti.hardware.qccsyshal@1.2-service.rc
system_ext/etc/init/vendor.qti.qccsyshal_aidl-service.rc
system_ext/etc/vintf/manifest/vendor.qti.qccsyshal_aidl-service.xml
```

#### Bibliotecas QCC 32-bit
```bash
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

#### Bibliotecas QCC 64-bit
```bash
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

**Función:** Conectividad vehicular, Android Auto, integración con pantallas del coche

---

### C. Digital Key - Servicio de Sincronización (3 archivos)

```bash
system_ext/priv-app/DckTimeSyncService
system_ext/priv-app/DckTimeSyncService/DckTimeSyncService.apk
system_ext/framework/org.carconnectivity.android.digitalkey.timesync.jar
```

**Función:** Sincronización de tiempo para llaves digitales (desbloqueo de coche con el teléfono)

---

## Resumen system_ext/

| Acción | Archivos | Impacto |
|--------|----------|---------|
| Eliminar | 1 | VNDK v31 |
| Copiar | 41 | VNDK v33 + QCC + Digital Key |
| **Total cambios** | **42** | - |

---

# PARTE 2: PARTICIÓN product/

## Análisis product/

**Estado actual:**
- r0q: 420 archivos
- dm2q: 433 archivos
- Comunes: 419 archivos (96.8%)

## 2.1 Archivos a ELIMINAR de product/ (1 archivo)

```bash
# Overlay específico de r0q
rm product/overlay/framework-res__r0qxxx__auto_generated_rro_product.apk
```

## 2.2 Archivos a COPIAR de dm2q a product/ (14 archivos)

### A. Assistant Shell (2 archivos)
```bash
product/app/AssistantShell
product/app/AssistantShell/AssistantShell.apk
```
**Función:** Shell del asistente de Google

---

### B. Overlays de Wi-Fi Avanzado (6 archivos)

#### Wi-Fi 6E (6 GHz)
```bash
product/overlay/SoftapOverlay6GHz
product/overlay/SoftapOverlay6GHz/SoftapOverlay6GHz.apk
```
**Función:** Habilita banda de 6 GHz para hotspot Wi-Fi 6E

#### Dual Access Point
```bash
product/overlay/SoftapOverlayDualAp
product/overlay/SoftapOverlayDualAp/SoftapOverlayDualAp.apk
```
**Función:** Permite crear dos puntos de acceso simultáneos

#### OWE (Opportunistic Wireless Encryption)
```bash
product/overlay/SoftapOverlayOWE
product/overlay/SoftapOverlayOWE/SoftapOverlayOWE.apk
```
**Función:** Cifrado Wi-Fi mejorado para redes públicas

---

### C. UWB - Ultra-Wideband (1 archivo)
```bash
product/overlay/UwbRROverlay.apk
```
**Función:** Overlay para UWB Ranging (localización precisa, llaves digitales)

---

### D. Overlay de Dispositivo (1 archivo)
```bash
product/overlay/framework-res__dm2qxxx__auto_generated_rro_product.apk
```
**Función:** Identificación del dispositivo como dm2q

---

## Resumen product/

| Acción | Archivos | Impacto |
|--------|----------|---------|
| Eliminar | 1 | Overlay r0q |
| Copiar | 14 | Wi-Fi 6E, UWB, Assistant |
| **Total cambios** | **15** | - |

---

# PARTE 3: PARTICIÓN system/

## Análisis system/

**Estado actual:**
- r0q: 7513 archivos
- dm2q: 7630 archivos
- Comunes: 7426 archivos (97.3%)

## 3.1 Archivos a ELIMINAR de system/ (87 archivos)

### A. Overlays de r0q (2 archivos)
```bash
rm system/vendor/overlay/framework-res__r0qxxx__auto_generated_rro_vendor.apk
```

### B. Bibliotecas de Seguridad Antiguas (12 archivos)

#### KeyMint V1 (obsoleto, dm2q usa V2)
```bash
rm system/lib/android.hardware.security.keymint-V1-ndk.so
rm system/lib64/android.hardware.security.keymint-V1-ndk.so
rm system/lib/vendor.samsung.hardware.keymint-V1-ndk.so
rm system/lib64/vendor.samsung.hardware.keymint-V1-ndk.so
```

#### HALs HIDL (obsoletos, dm2q usa AIDL)
```bash
rm system/lib/libsec_semHal.so
rm system/lib64/libsec_semHal.so
rm system/lib/libsec_skpmHal.so
rm system/lib64/libsec_skpmHal.so
rm system/lib/vendor.samsung.hardware.security.sem@1.0.so
rm system/lib64/vendor.samsung.hardware.security.sem@1.0.so
rm system/lib/vendor.samsung.hardware.security.skpm@1.0.so
rm system/lib64/vendor.samsung.hardware.security.skpm@1.0.so
```

**Impacto:** Evita conflictos de autenticación y cifrado

---

### C. Bibliotecas de Cámara SM8450 (8 archivos)

#### Datos de cámara Snapdragon 8 Gen 1
```bash
rm system/cameradata/portrait_data/SRIB_Acenet_A16W8_V141_sm8450_snpe2108.dlc
rm system/cameradata/portrait_data/SRIB_Matting_INT8_V015_sm8450_snpe2108_TILE_896.dlc
rm system/cameradata/portrait_data/SRIB_SID_A16W8_V018_sm8450_snpe2106.dlc
```

#### Bibliotecas de procesamiento
```bash
rm system/lib64/libHREnhancementAPI.camera.samsung.so
rm system/lib64/libarcsoft_superresolution_bokeh.so
rm system/lib64/libhigh_dynamic_range.arcsoft.so
rm system/lib64/libhighres_enhancement.arcsoft.so
rm system/lib64/liblow_light_hdr.arcsoft.so
```

**Impacto:** Evita crashes de cámara (dm2q usa SM8550)

---

### D. Servicios de Media Antiguos (6 archivos)
```bash
rm system/lib/libmediacaptureservice.so
rm system/lib64/libmediacaptureservice.so
rm system/lib/libmediaplayerservice.so
rm system/lib64/libmediaplayerservice.so
rm system/lib/libstagefright_httplive_sec.so
rm system/lib64/libstagefright_httplive_sec.so
```

**Impacto:** dm2q tiene versiones actualizadas para Android 13

---

### E. HALs Dumpstate (2 archivos)
```bash
rm system/lib64/android.hardware.dumpstate@1.0.so
rm system/lib64/android.hardware.dumpstate@1.1.so
```

---

### F. Aplicaciones Específicas de r0q (4 apps, ~24 archivos)
```bash
rm -rf system/app/Cameralyzer
rm -rf system/app/ClockPackage
rm -rf system/app/MinusOnePage
rm -rf system/app/SamsungTTS_no_vdata
```

**Impacto:** Evita conflictos con apps de dm2q

---

### G. Configuración Digital Key BLE (1 archivo)
```bash
rm system/etc/init/digitalkey_init_ble_tss2.rc
```

**Impacto:** dm2q usa UWB en lugar de BLE

---

### H. Daemon SDP (1 archivo)
```bash
rm system/bin/sdp_cryptod
```

---

## 3.2 Archivos a COPIAR de dm2q a system/ (204 archivos)

### A. CRÍTICOS - Overlays de Dispositivo (2 archivos)
```bash
system/vendor/overlay/framework-res__dm2qxxx__auto_generated_rro_vendor.apk
system/vendor/overlay/framework-res__dm1qxxx__auto_generated_rro_vendor.apk
```
**Función:** Identificación del dispositivo

---

### B. CRÍTICOS - Datos de Cámara SM8550 (5 archivos)
```bash
system/cameradata/portrait_data/SRIB_Acenet_A16W8_V141_sm8550_snpe2704.dlc
system/cameradata/portrait_data/SRIB_DPD_A16W8_V013_sm8550_snpe2106.dlc
system/cameradata/portrait_data/SRIB_HDE_A16W8_V003_sm8550_snpe2433.dlc
system/cameradata/portrait_data/SRIB_Matting_INT8_V015_sm8550_snpe2108_TILE_896.dlc
system/cameradata/portrait_data/SRIB_SID_A16W8_V018_sm8550_snpe2433.dlc
```
**Función:** Algoritmos de cámara para Snapdragon 8 Gen 2

---

### C. CRÍTICOS - Configuración UWB (3 archivos)
```bash
system/etc/libuwb-cal.conf
system/etc/init/init.system.uwb.rc
system/etc/init/digitalkey_init_uwb_tss2.rc
```
**Función:** Ultra-Wideband para localización precisa

---

### D. CRÍTICOS - Configuración dm2q (1 archivo)
```bash
system/etc/init/ssu_dm2qxxx.rc
```
**Función:** Inicialización específica de dm2q

---

### E. CRÍTICOS - Bibliotecas de Seguridad V2 (12 archivos)

#### KeyMint V2 (Android 13)
```bash
system/lib/android.hardware.security.keymint-V2-ndk.so
system/lib64/android.hardware.security.keymint-V2-ndk.so
system/lib/vendor.samsung.hardware.keymint-V2-ndk.so
system/lib64/vendor.samsung.hardware.keymint-V2-ndk.so
```

#### HALs AIDL (modernos)
```bash
system/lib/libsec_semAidl.so
system/lib64/libsec_semAidl.so
system/lib/libsec_skpmAidl.so
system/lib64/libsec_skpmAidl.so
system/lib/vendor.samsung.hardware.security.sem-V1-ndk.so
system/lib64/vendor.samsung.hardware.security.sem-V1-ndk.so
system/lib/vendor.samsung.hardware.security.skpm-V1-ndk.so
system/lib64/vendor.samsung.hardware.security.skpm-V1-ndk.so
```

**Función:** Autenticación y cifrado mejorados

---

### F. CRÍTICOS - Bibliotecas de Cámara y AI (26 archivos)

#### Procesamiento de Cámara Samsung
```bash
system/lib64/libDocDeblur.camera.samsung.so
system/lib64/libDocObjectRemoval.camera.samsung.so
system/lib64/libDocObjectRemoval.enhanceX.samsung.so
system/lib64/libSceneDetector_v1.camera.samsung.so
system/lib/libSemanticMap_v1.camera.samsung.so
system/lib64/libSemanticMap_v1.camera.samsung.so
system/lib/libSlowShutter-core.so
system/lib64/libSlowShutter-core.so
system/lib64/libWideDistortionCorrection.camera.samsung.so
```

#### AI y Arcsoft
```bash
system/lib64/libacz_hhdr.arcsoft.so
system/lib64/libaiclearzoom_raw.arcsoft.so
system/lib64/libaiclearzoomraw_wrapper_v1.camera.samsung.so
system/lib64/libface_recognition.arcsoft.so
system/lib64/libpic_best.arcsoft.so
```

#### FRC (Frame Rate Conversion)
```bash
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

**Función:** IA de cámara, detección de escenas, mejora de imágenes

---

### G. CRÍTICOS - Servicios de Media (3 archivos)
```bash
system/lib64/libmediacaptureservice.so
system/lib64/libmediaplayerservice.so
system/lib64/libstagefright_httplive_sec.so
```

**Función:** Captura y reproducción de media para Android 13

---

### H. CRÍTICOS - Audio Espacial (4 archivos)
```bash
system/lib/libswdapaidl.so
system/lib64/libswdapaidl.so
system/lib/libswspatializeraidl.so
system/lib64/libswspatializeraidl.so
```

**Función:** Audio espacial y DAP (Dolby Audio Processing)

---

### I. CRÍTICOS - UWB TensorFlow (2 archivos)
```bash
system/lib/libtflite_uwb_jni.so
system/lib64/libtflite_uwb_jni.so
```

**Función:** Machine Learning para UWB

---

### J. OPCIONALES - Samsung TTS con Voces (~150 archivos)

```bash
system/app/SamsungTTS
system/app/SamsungTTS/SamsungTTS.apk

# Paquetes de voz (12 idiomas):
system/app/SamsungTTSVoice_ar_AE_m00  # Árabe
system/app/SamsungTTSVoice_de_DE_f00  # Alemán
system/app/SamsungTTSVoice_en_GB_f00  # Inglés UK
system/app/SamsungTTSVoice_es_ES_f00  # Español España
system/app/SamsungTTSVoice_es_US_f00  # Español EEUU
system/app/SamsungTTSVoice_fr_FR_f00  # Francés
system/app/SamsungTTSVoice_hi_IN_f00  # Hindi
system/app/SamsungTTSVoice_id_ID_f00  # Indonesio
system/app/SamsungTTSVoice_it_IT_f00  # Italiano
system/app/SamsungTTSVoice_pl_PL_f00  # Polaco
system/app/SamsungTTSVoice_pt_BR_f00  # Portugués Brasil
system/app/SamsungTTSVoice_ru_RU_f00  # Ruso
system/app/SamsungTTSVoice_th_TH_f00  # Tailandés
system/app/SamsungTTSVoice_tr_TR_f00  # Turco
system/app/SamsungTTSVoice_vi_VN_f00  # Vietnamita
system/app/SamsungTTSVoice_zh_CN_m00  # Chino
```

**Opción:** Puedes NO instalar estos si prefieres ahorrar espacio (~200MB)

---

### K. OPCIONALES - Apps Adicionales (2 apps)
```bash
system/app/UwbTest
system/app/UwbTest/UwbTest.apk

system/app/SketchBook
system/app/SketchBook/SketchBook.apk
```

**Función:** Herramienta de prueba UWB + App de dibujo

---

### L. OPCIONALES - Búsqueda de Medios (7 archivos)
```bash
system/etc/mediasearch/data/dec_adaptor.tflite
system/etc/mediasearch/data/dec_event.tflite
system/etc/mediasearch/data/enc_image.tflite
system/etc/mediasearch/data/enc_text.tflite
system/etc/mediasearch/data/versioninfo.json
system/etc/default-permissions/default-permissions-com.samsung.mediasearch.xml
system/etc/default-permissions/default-permissions-com.samsung.videoscan.xml
```

**Función:** Búsqueda inteligente de fotos y videos

---

## Resumen system/

| Acción | Archivos | Categoría |
|--------|----------|-----------|
| Eliminar | 87 | KeyMint V1, SM8450, apps r0q |
| Copiar (críticos) | 52 | Overlays, cámara, UWB, seguridad |
| Copiar (opcionales) | 152 | TTS, apps, búsqueda |
| **Total cambios** | **239** | - |

---

# RESUMEN GENERAL DE PORTEO

## Cambios por Partición

| Partición | Eliminar | Copiar | Total |
|-----------|----------|--------|-------|
| **system_ext/** | 1 | 41 | 42 |
| **product/** | 1 | 14 | 15 |
| **system/** | 87 | 204 | 291 |
| **TOTAL** | **89** | **259** | **348** |

---

## Archivos Críticos (MÍNIMO NECESARIO)

### Instalación Mínima = 110 archivos

- system_ext: 41 archivos (VNDK + QCC)
- product: 14 archivos (Wi-Fi 6E, UWB)
- system: 52 archivos críticos (sin TTS completo)
- Eliminar: 89 archivos

### Instalación Completa = 348 archivos

- Incluye TODO lo anterior
- + 152 archivos opcionales (TTS completo, apps)

---

## Funcionalidad por Categoría

| Función | Archivos | Resultado si NO copias |
|---------|----------|------------------------|
| VNDK Android 13 | 1 | ❌ Sistema no arranca |
| Overlays dm2q | 4 | ❌ Detectado como r0q |
| Cámara SM8550 | 5 datos | ❌ Cámara no funciona |
| Seguridad V2 | 12 libs | ❌ Cifrado falla |
| UWB | 6 archivos | ⚠️ Sin llave digital UWB |
| QCC | 26 archivos | ⚠️ Sin Android Auto mejorado |
| Wi-Fi 6E | 2 overlays | ⚠️ Sin 6 GHz |
| TTS Completo | 150 archivos | ⚠️ Sin voces multiidioma |

---

## Orden de Operaciones Recomendado

```
1. ✅ Extraer particiones r0q (system, system_ext, product)
2. ✅ ELIMINAR 89 archivos de r0q (ver sección 3.1)
3. ✅ COPIAR 259 archivos de dm2q (ver secciones 1.2, 2.2, 3.2)
4. ✅ Verificar integridad
5. ✅ Reempaquetar particiones
6. ✅ Flashear: system_ext → product → system
7. ✅ Flashear vendor dm2q (ya lo tienes)
8. ✅ Wipe cache/dalvik
9. ✅ Primer arranque (10-15 minutos)
```

---

## Scripts de Verificación

### Verificar Eliminaciones
```bash
# No debe existir VNDK v31
[ ! -f system_ext/apex/com.android.vndk.v31.apex ] && echo "✓ VNDK v31 eliminado" || echo "✗ ERROR"

# No deben existir KeyMint V1
[ ! -f system/lib/android.hardware.security.keymint-V1-ndk.so ] && echo "✓ KeyMint V1 eliminado" || echo "✗ ERROR"

# No deben existir datos SM8450
[ ! -f system/cameradata/portrait_data/SRIB_*sm8450*.dlc ] && echo "✓ Cámara SM8450 eliminada" || echo "✗ ERROR"
```

### Verificar Copias
```bash
# Debe existir VNDK v33
[ -f system_ext/apex/com.android.vndk.v33.apex ] && echo "✓ VNDK v33 presente" || echo "✗ ERROR"

# Deben existir overlays dm2q
[ -f product/overlay/framework-res__dm2qxxx__auto_generated_rro_product.apk ] && echo "✓ Overlay dm2q presente" || echo "✗ ERROR"

# Deben existir datos SM8550
[ -f system/cameradata/portrait_data/SRIB_Acenet_A16W8_V141_sm8550_snpe2704.dlc ] && echo "✓ Cámara SM8550 presente" || echo "✗ ERROR"
```

---

## Problemas Comunes y Soluciones

### Problema: Sistema no arranca
**Causa:** VNDK v31 no eliminado o v33 no instalado
**Solución:** Verificar system_ext/apex/

### Problema: Cámara crashea
**Causa:** Datos SM8450 aún presentes o SM8550 no copiados
**Solución:** Verificar system/cameradata/portrait_data/

### Problema: Autenticación falla
**Causa:** KeyMint V1 y V2 en conflicto
**Solución:** Eliminar TODAS las libs keymint-V1-ndk.so

### Problema: Wi-Fi 6 GHz no aparece
**Causa:** Overlay SoftapOverlay6GHz no instalado
**Solución:** Copiar product/overlay/SoftapOverlay6GHz/

### Problema: UWB no funciona
**Causa:** Configuración faltante
**Solución:** Copiar system/etc/libuwb-cal.conf y archivos relacionados

---

## Tamaño Estimado de Cambios

- Archivos a eliminar: ~50 MB
- Archivos críticos a copiar: ~180 MB
- TTS completo (opcional): ~200 MB
- **Total neto:** +130 MB (sin TTS) o +330 MB (con TTS)

---

## Conclusión

Esta guía cubre las **3 particiones** (system, system_ext, product) necesarias para el porteo.

**Recuerda:**
- ✅ vendor/ ya está instalado de dm2q
- ✅ Hacer backup antes de empezar
- ✅ Los cambios son reversibles
- ⚠️ Riesgo de brick si se hace mal

**Éxito del porteo depende de:**
1. Eliminar correctamente los 89 archivos de r0q
2. Copiar los 259 archivos de dm2q (mínimo 110)
3. Verificar integridad antes de flashear
