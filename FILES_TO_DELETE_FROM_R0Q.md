# Archivos a ELIMINAR de r0q

Esta lista contiene TODOS los archivos que debes eliminar de r0q antes de instalar los componentes de dm2q.

**⚠️ IMPORTANTE:** Elimina estos archivos ANTES de copiar los de dm2q para evitar conflictos.

---

## CRÍTICOS - DEBEN ELIMINARSE

### 1. VNDK Antiguo (Android 12)

```
system_ext/apex/com.android.vndk.v31.apex
```

**Razón:** Incompatible con Android 13 (dm2q usa VNDK v33)

---

### 2. Overlays Específicos de r0q

```
product/overlay/framework-res__r0qxxx__auto_generated_rro_product.apk

system/vendor/overlay/framework-res__r0qxxx__auto_generated_rro_vendor.apk
```

**Razón:** Causan identificación incorrecta del dispositivo. dm2q usa sus propios overlays.

---

### 3. Bibliotecas de Seguridad Antiguas (KeyMint V1 → V2)

#### Bibliotecas KeyMint V1 (OBSOLETAS)
```
system/lib/android.hardware.security.keymint-V1-ndk.so
system/lib64/android.hardware.security.keymint-V1-ndk.so

system/lib/vendor.samsung.hardware.keymint-V1-ndk.so
system/lib64/vendor.samsung.hardware.keymint-V1-ndk.so
```

#### HALs de Seguridad HIDL (OBSOLETOS, cambio a AIDL)
```
system/lib/libsec_semHal.so
system/lib64/libsec_semHal.so

system/lib/libsec_skpmHal.so
system/lib64/libsec_skpmHal.so

system/lib/vendor.samsung.hardware.security.sem@1.0.so
system/lib64/vendor.samsung.hardware.security.sem@1.0.so

system/lib/vendor.samsung.hardware.security.skpm@1.0.so
system/lib64/vendor.samsung.hardware.security.skpm@1.0.so
```

**Razón:** dm2q usa KeyMint V2 con AIDL. Las versiones V1 y HIDL causan conflictos de autenticación.

**Total:** 12 archivos

---

### 4. Bibliotecas de Cámara SM8450 (Incompatibles con SM8550)

#### Datos de Cámara para Snapdragon 8 Gen 1
```
system/cameradata/portrait_data/SRIB_Acenet_A16W8_V141_sm8450_snpe2108.dlc
system/cameradata/portrait_data/SRIB_Matting_INT8_V015_sm8450_snpe2108_TILE_896.dlc
system/cameradata/portrait_data/SRIB_SID_A16W8_V018_sm8450_snpe2106.dlc
```

#### Bibliotecas de Procesamiento de Cámara
```
system/lib64/libHREnhancementAPI.camera.samsung.so
system/lib64/libarcsoft_superresolution_bokeh.so
system/lib64/libhigh_dynamic_range.arcsoft.so
system/lib64/libhighres_enhancement.arcsoft.so
system/lib64/liblow_light_hdr.arcsoft.so
```

**Razón:** dm2q usa SM8550 (Snapdragon 8 Gen 2). Los archivos de SM8450 causan crashes de cámara.

**Total:** 8 archivos

---

### 5. Bibliotecas de Media y Servicios (Versiones Antiguas)

```
system/lib/libmediacaptureservice.so
system/lib64/libmediacaptureservice.so

system/lib/libmediaplayerservice.so
system/lib64/libmediaplayerservice.so

system/lib/libstagefright_httplive_sec.so
system/lib64/libstagefright_httplive_sec.so
```

**Razón:** dm2q tiene versiones actualizadas para Android 13.

**Total:** 6 archivos

---

### 6. HALs de Dumpstate Antiguos

```
system/lib64/android.hardware.dumpstate@1.0.so
system/lib64/android.hardware.dumpstate@1.1.so
```

**Razón:** dm2q usa versiones más recientes integradas.

**Total:** 2 archivos

---

## OPCIONALES - Pueden Eliminarse

### 7. Aplicaciones Específicas de r0q

```
system/app/Cameralyzer
system/app/Cameralyzer/Cameralyzer.apk

system/app/ClockPackage
system/app/ClockPackage/ClockPackage.apk

system/app/MinusOnePage
system/app/MinusOnePage/MinusOnePage.apk
```

**Razón:** Herramientas específicas de r0q que pueden conflictuar con dm2q.

**Total:** 3 apps (6 archivos sin contar oat/)

---

### 8. TTS Ligero de r0q (Si instalas TTS completo de dm2q)

```
system/app/SamsungTTS_no_vdata
system/app/SamsungTTS_no_vdata/SamsungTTS_no_vdata.apk
```

**Razón:** dm2q tiene TTS completo con paquetes de voz. Esta versión ligera no es necesaria.

**Total:** 1 app (2 archivos sin contar oat/)

---

### 9. Configuración de Digital Key BLE

```
system/etc/init/digitalkey_init_ble_tss2.rc
```

**Razón:** dm2q usa UWB para Digital Key (`digitalkey_init_uwb_tss2.rc`). Ambos pueden conflictuar.

**Total:** 1 archivo

---

## MANTENER (NO Eliminar)

### Bibliotecas SDP (Sensitive Data Protection)

```
system/lib/libsdp_crypto.so
system/lib64/libsdp_crypto.so
system/lib/libsdp_kekm.so
system/lib64/libsdp_kekm.so
system/lib/libsdp_sdk.so
system/lib64/libsdp_sdk.so
system/bin/sdp_cryptod
```

**Razón:** Estas bibliotecas de r0q pueden seguir funcionando. dm2q maneja SDP de forma diferente pero son compatibles. Solo elimínalas si causan problemas específicos.

**Total:** 7 archivos (MANTENER a menos que causen conflictos)

---

### Otras Bibliotecas de r0q

```
system/lib/libmdfpp_req.so
system/lib64/libmdfpp_req.so
```

**Razón:** Bibliotecas específicas de r0q que no están en dm2q. Mantenerlas no causa problemas.

**Total:** 2 archivos (MANTENER)

---

## RESUMEN DE ARCHIVOS A ELIMINAR

| Categoría | Archivos | Prioridad |
|-----------|----------|-----------|
| VNDK v31 | 1 | ✅ CRÍTICO |
| Overlays r0q | 2 | ✅ CRÍTICO |
| KeyMint V1 + HIDL HALs | 12 | ✅ CRÍTICO |
| Cámara SM8450 | 8 | ✅ CRÍTICO |
| Media services antiguos | 6 | ✅ CRÍTICO |
| Dumpstate HALs | 2 | ✅ CRÍTICO |
| Apps específicas r0q | 3 apps | 🔶 OPCIONAL |
| TTS ligero | 1 app | 🔶 OPCIONAL |
| Digital Key BLE config | 1 | 🔶 OPCIONAL |
| **TOTAL CRÍTICO** | **31 archivos** | - |
| **TOTAL OPCIONAL** | **5 apps/archivos** | - |
| **TOTAL A ELIMINAR** | **~36 archivos** | - |

---

## Comando para Eliminar (Ejemplo)

Si estás trabajando con las particiones extraídas:

```bash
# Eliminar VNDK v31
rm system_ext/apex/com.android.vndk.v31.apex

# Eliminar overlays de r0q
rm product/overlay/framework-res__r0qxxx__auto_generated_rro_product.apk
rm system/vendor/overlay/framework-res__r0qxxx__auto_generated_rro_vendor.apk

# Eliminar KeyMint V1 y HALs HIDL
rm system/lib/android.hardware.security.keymint-V1-ndk.so
rm system/lib64/android.hardware.security.keymint-V1-ndk.so
rm system/lib/vendor.samsung.hardware.keymint-V1-ndk.so
rm system/lib64/vendor.samsung.hardware.keymint-V1-ndk.so
rm system/lib/libsec_semHal.so
rm system/lib64/libsec_semHal.so
rm system/lib/libsec_skpmHal.so
rm system/lib64/libsec_skpmHal.so
rm system/lib/vendor.samsung.hardware.security.sem@1.0.so
rm system/lib64/vendor.samsung.hardware.security.sem@1.0.so
rm system/lib/vendor.samsung.hardware.security.skpm@1.0.so
rm system/lib64/vendor.samsung.hardware.security.skpm@1.0.so

# Eliminar datos de cámara SM8450
rm system/cameradata/portrait_data/SRIB_Acenet_A16W8_V141_sm8450_snpe2108.dlc
rm system/cameradata/portrait_data/SRIB_Matting_INT8_V015_sm8450_snpe2108_TILE_896.dlc
rm system/cameradata/portrait_data/SRIB_SID_A16W8_V018_sm8450_snpe2106.dlc
rm system/lib64/libHREnhancementAPI.camera.samsung.so
rm system/lib64/libarcsoft_superresolution_bokeh.so
rm system/lib64/libhigh_dynamic_range.arcsoft.so
rm system/lib64/libhighres_enhancement.arcsoft.so
rm system/lib64/liblow_light_hdr.arcsoft.so

# Eliminar servicios de media antiguos
rm system/lib/libmediacaptureservice.so
rm system/lib64/libmediacaptureservice.so
rm system/lib/libmediaplayerservice.so
rm system/lib64/libmediaplayerservice.so
rm system/lib/libstagefright_httplive_sec.so
rm system/lib64/libstagefright_httplive_sec.so

# Eliminar HALs dumpstate
rm system/lib64/android.hardware.dumpstate@1.0.so
rm system/lib64/android.hardware.dumpstate@1.1.so

# OPCIONAL: Eliminar apps específicas de r0q
rm -rf system/app/Cameralyzer
rm -rf system/app/ClockPackage
rm -rf system/app/MinusOnePage
rm -rf system/app/SamsungTTS_no_vdata

# OPCIONAL: Eliminar config Digital Key BLE
rm system/etc/init/digitalkey_init_ble_tss2.rc
```

---

## Verificación

Después de eliminar, verifica que no existan:

```bash
# Verifica VNDK
ls system_ext/apex/com.android.vndk.v31.apex 2>/dev/null && echo "ERROR: VNDK v31 aún existe" || echo "OK"

# Verifica KeyMint V1
ls system/lib*/android.hardware.security.keymint-V1-ndk.so 2>/dev/null && echo "ERROR: KeyMint V1 aún existe" || echo "OK"

# Verifica overlays r0q
ls product/overlay/framework-res__r0qxxx__* 2>/dev/null && echo "ERROR: Overlay r0q existe" || echo "OK"
```

---

## Orden Recomendado de Operaciones

1. ✅ **Eliminar archivos de r0q** (este documento)
2. ✅ **Copiar archivos de dm2q** (ver FILES_TO_COPY_FROM_DM2Q.md)
3. ✅ **Verificar no hay conflictos**
4. ✅ **Flashear particiones**

**IMPORTANTE:** Siempre haz backup completo antes de empezar.
