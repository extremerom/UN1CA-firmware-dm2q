# Análisis de Ingeniería Inversa - Firmware Samsung Galaxy S23 (SM-S916B)

## Información General del Firmware

**Dispositivo**: Samsung Galaxy S23 (dm2q - SM-S916B)
**Versión Android**: 36 (Android 14/15 Beta)
**Versión de Compilación**: S916BXXS8EYK5
**Fecha de Compilación**: Fri Nov 28 10:13:24 KST 2025
**Tipo de Compilación**: user/release-keys
**Region**: XXX (Multi-CSC Europa)

## 1. Funcionalidades Ocultas Descubiertas

### 1.1 Aplicaciones Ocultas en `/system/system/hidden/`

Se encontró un directorio oculto con aplicaciones no visibles en el sistema:

- **SmartTutor** (24.5 MB)
  - Ubicación: `/system/system/hidden/SmartTutor/SmartTutor.apk`
  - Función: Herramienta de soporte remoto de Samsung
  - Posible uso: Diagnóstico y soporte técnico remoto

- **INTERNAL_SDCARD**
  - Ubicación: `/system/system/hidden/INTERNAL_SDCARD/`
  - Función: Posible almacenamiento interno oculto

### 1.2 Aplicaciones de Test y Diagnóstico

#### Aplicaciones Privilegiadas (priv-app):

1. **FactoryTestProvider** (`/system/system/priv-app/FactoryTestProvider/`)
   - Proveedor de tests de fábrica
   - Acceso privilegiado al sistema

2. **SecFactoryPhoneTest** (`/system/system/priv-app/SecFactoryPhoneTest/`)
   - Tests de hardware del teléfono
   - Funcionalidad de diagnóstico completo

3. **SmartEpdgTestApp** (`/system/system/priv-app/SmartEpdgTestApp/`)
   - Test de ePDG (evolved Packet Data Gateway)
   - Pruebas de conectividad VoLTE/VoWiFi

4. **EnhancedAttestationAgent** (`/system/system/priv-app/EnhancedAttestationAgent/`)
   - Agente de certificación mejorada
   - Relacionado con seguridad y verificación de integridad

5. **DiagMonAgent95** (`/system/system/priv-app/DiagMonAgent95/`)
   - Agente de monitoreo y diagnóstico
   - Posible telemetría y logging

6. **SEMFactoryApp** (`/system/system/priv-app/SEMFactoryApp/`)
   - Aplicación de fábrica Samsung
   - Tests y calibración de hardware

7. **NetworkDiagnostic** (`/system/system/priv-app/NetworkDiagnostic/`)
   - Diagnóstico de red
   - Tests de conectividad

8. **DeviceDiagnostics** (`/system/system/priv-app/DeviceDiagnostics/`)
   - Diagnóstico general del dispositivo
   - Tests de sensores y componentes

#### Aplicaciones de Sistema (app):

1. **UwbTest** (`/system/system/app/UwbTest/`)
   - Test de Ultra-Wideband (UWB)
   - Pruebas de conectividad espacial

2. **WlanTest** (`/system/system/app/WlanTest/`)
   - Test de WiFi/WLAN
   - Diagnóstico de conectividad inalámbrica

## 2. Herramientas de Diagnóstico Qualcomm

### 2.1 Binarios de Diagnóstico en `/vendor/bin/`

Se encontraron múltiples herramientas de diagnóstico Qualcomm:

- **debug-diag**: Herramienta de depuración principal
- **test_diag**: Test de diagnóstico
- **diag_uart_log**: Logs UART para diagnóstico
- **ipacm-diag**: Diagnóstico IPA (Internet Packet Accelerator)
- **diag_klog**: Logs del kernel
- **diag-router**: Enrutador de diagnóstico
- **ssr_diag**: Diagnóstico SSR (Subsystem Restart)
- **cnss_diag**: Diagnóstico CNSS (Connectivity Subsystem)

### 2.2 Librerías de Diagnóstico

Ubicadas en `/vendor/lib/` y `/vendor/lib64/`:

- `libdiagjni.so`: Interface JNI para diagnóstico
- `vendor.qti.diaghal@1.0.so`: HAL de diagnóstico Qualcomm
- `libdiag.so`: Librería principal de diagnóstico
- `libsnsdiaglog.so`: Logging de diagnóstico de sensores

### 2.3 Servicios de Diagnóstico

- `/vendor/etc/init/vendor.qti.diag.rc`: Servicio de diagnóstico
- `/vendor/etc/init/ipacm-diag.rc`: Servicio IPA diagnostic

## 3. Sistema de Seguridad Samsung Knox

### 3.1 Componentes Knox Encontrados

#### Frameworks:
- `knoxsdk.jar`: SDK principal de Knox
- `knoxanalyticssdk.jar`: SDK de analytics Knox
- `knox_mtd.jar`: Knox Mobile Threat Defense

#### Librerías Nativas:
- `libknoxnative_shared.so`: Librería nativa compartida
- `libknox_filemanager.so`: Gestor de archivos Knox
- `libknox_remotedesktopclient.knox.samsung.so`: Cliente de escritorio remoto

#### Permisos y Configuraciones:
- Múltiples archivos de permisos en `/system/system/etc/permissions/`
- `knox_sdk_api_level_39.xml`: API Level 39 de Knox
- Permisos privilegiados para varios componentes Knox

### 3.2 Características de Seguridad

- **Knox SDK**: Sistema completo de seguridad empresarial
- **Knox Analytics**: Telemetría y análisis de seguridad
- **Knox MTD**: Defensa contra amenazas móviles
- **Knox Attestation**: Sistema de certificación de integridad
- **Knox Network Filter**: Filtrado de red

## 4. Códigos Secretos (SECRET_CODE)

El sistema tiene soporte para códigos secretos mediante:

**Broadcast Action**: `android.telephony.action.SECRET_CODE`

Configuración en: `/system/system/etc/sysconfig/framework-sysconfig.xml`

Esto permite la activación de funciones ocultas mediante códigos USSD/MMI ingresados en el dialer.

### Códigos comunes de Samsung (requieren verificación):
- `*#0*#`: Test de hardware general
- `*#*#4636#*#*`: Información del teléfono
- `*#9900#`: SysDump mode
- `*#0228#`: Battery status
- `*#12580*369#`: SW & HW Info

## 5. Módulos del Kernel

### 5.1 Módulos de Dump y Diagnóstico

Ubicados en `/vendor_dlkm/lib/modules/`:

- **microdump_collector.ko**: Recolector de micro dumps
- **qcom_ramdump.ko**: RAM dump de Qualcomm
- **qcom_va_minidump.ko**: Mini dump de análisis de vulnerabilidad
- **dmesg_dumper.ko**: Dumper de dmesg
- **dropdump.ko**: Drop dump collector
- **sec_tsp_dumpkey.ko**: Dump key del touchscreen Samsung

### 5.2 Total de Módulos
- **366 módulos del kernel** en particiones DLKM
- Distribuidos entre `system_dlkm` y `vendor_dlkm`

## 6. Capacidades de Desarrollo y Depuración

### 6.1 Estado de Depuración
```properties
ro.debuggable=0
ro.force.debuggable=0
ro.adb.secure=1
```

El dispositivo está configurado en modo **no depurable** (producción):
- No se puede hacer root fácilmente
- ADB está en modo seguro (requiere autorización)
- Compilación firmada con release-keys

### 6.2 Scripts de Inicialización

Múltiples scripts en `/vendor/bin/` para:
- Inicialización del sistema
- Configuración de módulos
- Depuración de sensores
- Configuración de medios
- Post-boot configuration

## 7. Contenido del Archivo exS.zip

**Archivo**: `exS.zip` (17.7 MB)
**Contenido**: Samsung Smart Switch PC App / FUS Service
**Total de archivos**: 113 archivos

### Componentes principales:
- AdminDelegator.exe
- AdminDelegator_SmartSwitch.exe
- AgentModule.dll
- FUSServiceHelper.exe
- SmartSwitchPDLR.exe
- Múltiples librerías de idiomas
- Recursos y dependencias VC90

**Función**: Herramientas de actualización y gestión del firmware desde PC

## 8. Imágenes y Particiones

### 8.1 Imágenes del Kernel
- `boot.img`: Imagen de arranque
- `dtbo.img`: Device Tree Blob Overlay
- `init_boot.img`: Imagen de init boot
- `vendor_boot.img`: Boot del vendor

### 8.2 Verified Boot (AVB)
- `vbmeta.img`: Metadata de verified boot
- `vbmeta_patched.img`: Versión parcheada (posiblemente para root)

## 9. Características Interesantes de Hardware

### 9.1 Librerías de Cámara Samsung
- `libBeauty_v4.camera.samsung.so`: Modo belleza v4
- `libAIMFISP.camera.samsung.so`: ISP con IA
- `libOpenCv.camera.samsung.so`: OpenCV para cámara
- `libPersonal_capture.camera.samsung.so`: Captura personalizada
- `libMoireDetection.camera.samsung.so`: Detección de moiré
- `libLightObjectDetector_v1.camera.samsung.so`: Detector de objetos con IA
- `libHprFace_GAE_api.camera.samsung.so`: API facial avanzada

### 9.2 Características de Audio
- `libaudiosaplus_sec.so`: Audio SA Plus Samsung
- `libsamsungSoundbooster_plus.so`: Sound Booster Plus

### 9.3 Biometría
- `vendor.samsung.hardware.biometrics.fingerprint-V1-ndk.so`
- Soporte completo de huella dactilar

### 9.4 Blockchain y TLC
- `vendor.samsung.hardware.tlc.blockchain@1.0.so`
- Soporte de blockchain a nivel de hardware
- TLC (Trusted Logic Client) para seguridad

## 10. Configuraciones del Sistema

### 10.1 Total de APKs
**477 aplicaciones** instaladas en el firmware

### 10.2 Particiones
- **system**: Sistema base Android
- **product**: Aplicaciones de producto
- **vendor**: Componentes específicos del fabricante
- **odm**: Customización OEM
- **system_ext**: Extensiones del sistema
- **system_dlkm**: Módulos del kernel del sistema
- **vendor_dlkm**: Módulos del kernel del vendor

### 10.3 Contextos de Seguridad SELinux
Múltiples archivos `file_context-*` para cada partición, indicando:
- Políticas SELinux estrictas
- Separación de contextos por partición
- Protección avanzada del sistema

## 11. Conclusiones y Observaciones

### 11.1 Nivel de Seguridad
- **Alto**: Knox activo, SELinux enforcing, verified boot
- Múltiples capas de seguridad a nivel de hardware y software
- Firmware firmado con release-keys

### 11.2 Funcionalidades Ocultas Significativas
1. **Diagnóstico Completo**: Acceso a herramientas de diagnóstico a nivel de chip
2. **Tests de Fábrica**: Múltiples apps de test no accesibles normalmente
3. **Smart Tutor Oculto**: Soporte remoto pre-instalado pero oculto
4. **Códigos Secretos**: Sistema de activación de funciones mediante códigos

### 11.3 Capacidades de Ingeniería
- Soporte completo para diagnóstico Qualcomm
- Herramientas de dump y análisis de crashes
- Módulos de kernel para debugging
- Scripts de inicialización configurables

### 11.4 Características Avanzadas
- **IA en Cámara**: Múltiples librerías de procesamiento con IA
- **Blockchain**: Soporte nativo de blockchain
- **UWB**: Tecnología Ultra-Wideband para posicionamiento preciso
- **Knox Enterprise**: Suite completa de seguridad empresarial

### 11.5 Potencial de Modificación
- **Limitado**: Debido a verified boot y firmas
- **Posible con vbmeta parcheado**: Se encontró `vbmeta_patched.img`
- **Requiere unlock del bootloader**: Para modificaciones significativas

## 12. Recomendaciones para Desarrollo/Research

### 12.1 Áreas de Interés
1. Analizar APKs de test con herramientas como apktool/jadx
2. Investigar códigos secretos funcionales
3. Estudiar librerías de cámara con IA
4. Examinar implementación de Knox y TrustZone
5. Analizar módulos del kernel para debugging

### 12.2 Herramientas Sugeridas
- **APKTool**: Descompilar APKs
- **JADX**: Decompilación a Java
- **Ghidra/IDA**: Análisis de binarios nativos
- **Wireshark**: Análisis de tráfico de diagnóstico
- **Frida**: Hooking dinámico en runtime

### 12.3 Vectores de Investigación
1. Activación de apps ocultas mediante actividades específicas
2. Explotación de interfaces de diagnóstico Qualcomm
3. Análisis de implementación de Knox SDK
4. Reverse engineering de algoritmos de cámara IA
5. Estudio de módulos de dump para forensics

---

**Documento generado**: 2025-12-28
**Versión del firmware analizado**: S916BXXS8EYK5
**Dispositivo**: Samsung Galaxy S23 (SM-S916B)
**Estado**: Análisis preliminar completado
