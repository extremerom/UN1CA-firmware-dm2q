# Dependencias de Aplicaciones de Fábrica y Diagnóstico

Este documento lista todas las dependencias (XML, binarios, librerías, etc.) para las aplicaciones de fábrica y diagnóstico del firmware UN1CA-firmware-dm2q.

## Resumen Rápido

| # | Aplicación | Paquete | Ubicación | Tipo |
|---|-----------|---------|-----------|------|
| 1 | ModemServiceMode | com.sec.android.RilServiceModeApp | /system/priv-app/ | Privilegiada |
| 2 | SecFactoryPhoneTest | - | /system/priv-app/ | Privilegiada |
| 3 | DiagMonAgent95 | com.sec.android.diagmonagent | /system/priv-app/ | Privilegiada |
| 4 | DeviceDiagnostics | - | /system/priv-app/ | Privilegiada |
| 5 | NetworkDiagnostic | com.samsung.android.networkdiagnostic | /system/priv-app/ | Privilegiada |
| 6 | SEMFactoryApp | com.sem.factoryapp | /system/priv-app/ | Privilegiada |
| 7 | SmartEpdgTestApp | com.sec.epdgtestapp | /system/priv-app/ | Privilegiada |
| 8 | FactoryTestProvider | com.samsung.android.providers.factory | /system/priv-app/ | Privilegiada |
| 9 | FactoryCameraFB | - | /system/app/ | Sistema |
| 10 | FactoryAirCommandManager | - | /system/app/ | Sistema |
| 11 | UwbTest | com.sec.android.app.uwbtest | /system/app/ | Sistema |
| 12 | WlanTest | - | /system/app/ | Sistema |

---

## 1. ModemServiceMode (Modo de Servicio del Módem)

### Información Básica
- **Ubicación**: `/system/priv-app/ModemServiceMode/ModemServiceMode.apk`
- **Paquete**: `com.sec.android.RilServiceModeApp`
- **Tipo**: Aplicación privilegiada del sistema

### Archivos APK y Optimizaciones
- `/system/priv-app/ModemServiceMode/ModemServiceMode.apk`
- `/system/priv-app/ModemServiceMode/oat/arm64/ModemServiceMode.odex`
- `/system/priv-app/ModemServiceMode/oat/arm64/ModemServiceMode.vdex`

### Permisos XML
- `/system/etc/permissions/privapp-permissions-com.sec.android.RilServiceModeApp.xml`
  - `android.permission.ACCESS_CHECKIN_PROPERTIES`
  - `android.permission.CHANGE_CONFIGURATION`
  - `android.permission.MODIFY_PHONE_STATE`
  - `android.permission.MOUNT_UNMOUNT_FILESYSTEMS`
  - `android.permission.WRITE_APN_SETTINGS`
  - `android.permission.READ_PRIVILEGED_PHONE_STATE`
  - `android.permission.ACCESS_FINE_LOCATION`
  - `android.permission.SET_DEBUG_APP`

### Configuración del Sistema
- Listado en `/system/etc/apks_count_list.txt`
- Listado en `/system/etc/irremovable_list.txt`

### Librerías RIL (Radio Interface Layer)
#### System Libraries
- `/system/lib/libsec_semRil.so`
- `/system/lib/libsecril-client.so`
- `/system/lib64/libsec_semRil.so`
- `/system/lib64/librildump_jni.so`
- `/system/lib64/libsecril-client.so`

#### Vendor Libraries
- `/vendor/lib/libsec_semRil.so`
- `/vendor/lib/libsecril-client.so`
- `/vendor/lib64/libsec-ril.so`
- `/vendor/lib64/libsec_semRil.so`
- `/vendor/lib64/libnetmgrmodemproxy.so`
- `/vendor/lib64/libsecril-client.so`
- `/vendor/lib64/librilutils.so`
- `/vendor/lib64/libril_sem.so`

### SELinux File Contexts
Todos los archivos de esta aplicación tienen el contexto SELinux `u:object_r:system_file:s0` definido en `file_context-system`.

---

## 2. SecFactoryPhoneTest (Prueba de Teléfono de Fábrica)

### Información Básica
- **Ubicación**: `/system/priv-app/SecFactoryPhoneTest/SecFactoryPhoneTest.apk`
- **Tipo**: Aplicación privilegiada del sistema

### Archivos APK y Optimizaciones
- `/system/priv-app/SecFactoryPhoneTest/SecFactoryPhoneTest.apk`
- `/system/priv-app/SecFactoryPhoneTest/oat/arm64/SecFactoryPhoneTest.odex`
- `/system/priv-app/SecFactoryPhoneTest/oat/arm64/SecFactoryPhoneTest.vdex`

### Configuración del Sistema
- Listado en `/system/etc/apks_count_list.txt`
- Listado en `/system/etc/irremovable_list.txt`

---

## 3. DiagMonAgent95 (Agente de Monitoreo de Diagnóstico)

### Información Básica
- **Ubicación**: `/system/priv-app/DiagMonAgent95/DiagMonAgent95.apk`
- **Paquete**: `com.sec.android.diagmonagent`
- **Tipo**: Aplicación privilegiada del sistema

### Archivos APK y Optimizaciones
- `/system/priv-app/DiagMonAgent95/DiagMonAgent95.apk`
- `/system/priv-app/DiagMonAgent95/oat/arm64/DiagMonAgent95.odex`
- `/system/priv-app/DiagMonAgent95/oat/arm64/DiagMonAgent95.vdex`

### Permisos XML
- `/system/etc/permissions/privapp-permissions-com.sec.android.diagmonagent.xml`
  - `android.permission.CHANGE_CONFIGURATION`
  - `android.permission.MODIFY_PHONE_STATE`
  - `android.permission.REAL_GET_TASKS`
  - `android.permission.PACKAGE_USAGE_STATS`
  - `com.sec.android.diagmonagent.permission.PROVIDER`
  - `com.sec.android.diagmonagent.permission.DIAGMON_SURVEY`
  - `android.permission.READ_PRIVILEGED_PHONE_STATE`
  - `android.permission.READ_LOGS`
  - `android.permission.READ_DROPBOX_DATA`
  - `com.samsung.permission.HQM_NOTIFICATION_PERMISSION`

### Configuración del Sistema
- Listado en `/system/etc/apks_count_list.txt`
- Listado en `/system/etc/irremovable_list.txt`

### Librerías Relacionadas
#### System Libraries
- `/system/lib/vendor.qti.diaghal-V1-ndk.so`
- `/system/lib64/vendor.qti.diaghal-V1-ndk.so`

#### System_ext Libraries
- `/system_ext/lib/vendor.qti.diaghal@1.0.so`
- `/system_ext/lib/libdiag_system.qti.so`
- `/system_ext/lib/libdiag_system.so`
- `/system_ext/lib64/vendor.qti.diaghal@1.0.so`
- `/system_ext/lib64/libdiag_system.qti.so`
- `/system_ext/lib64/libdiag_system.so`

#### Vendor Libraries
- `/vendor/lib/vendor.qti.diaghal@1.0.so`
- `/vendor/lib/libdiag.so`
- `/vendor/lib/libdiagjni.so`
- `/vendor/lib/libsnsdiaglog.so`
- `/vendor/lib64/vendor.qti.diaghal@1.0.so`
- `/vendor/lib64/libdiag.so`
- `/vendor/lib64/libdiagjni.so`
- `/vendor/lib64/libsnsdiaglog.so`

### Binarios
#### System Binaries
- `/system/bin/diagsylincom`
- `/system/bin/sec_diag_uart_log`

#### Vendor Binaries
- `/vendor/bin/debug-diag`
- `/vendor/bin/test_diag`
- `/vendor/bin/diag_uart_log`
- `/vendor/bin/ipacm-diag`
- `/vendor/bin/diag_klog`
- `/vendor/bin/diag-router`
- `/vendor/bin/ssr_diag`
- `/vendor/bin/cnss_diag`
- `/vendor/bin/diag_callback_sample`
- `/vendor/bin/diag_dci_sample`
- `/vendor/bin/diag_mdlog`
- `/vendor/bin/diag_socket_log`
- `/vendor/bin/athdiag`

### Init Services (RC Files)
- `/system/etc/init/diagsylincom.rc`
  - Service: `sylincom_modem_service`
- `/vendor/etc/init/vendor.qti.diag.rc`
  - Service: `vendor.diag-router`
- `/vendor/etc/init/ipacm-diag.rc`

### Permisos Especiales
- `/system/etc/permissions/com.qualcomm.qcom_diag.xml`
  - `com.qualcomm.permission.QCOM_DIAG`
  - Group IDs: `oem_2901`, `oem_2902`, `oem_2905`, `diag`

---

## 4. DeviceDiagnostics (Diagnóstico de Dispositivo)

### Información Básica
- **Ubicación**: `/system/priv-app/DeviceDiagnostics/DeviceDiagnostics.apk`
- **Tipo**: Aplicación privilegiada del sistema

### Archivos APK y Optimizaciones
- `/system/priv-app/DeviceDiagnostics/DeviceDiagnostics.apk`
- `/system/priv-app/DeviceDiagnostics/oat/arm64/DeviceDiagnostics.odex`
- `/system/priv-app/DeviceDiagnostics/oat/arm64/DeviceDiagnostics.vdex`

### Configuración del Sistema
- Listado en `/system/etc/apks_count_list.txt`
- Listado en `/system/etc/irremovable_list.txt`

---

## 5. NetworkDiagnostic (Diagnóstico de Red)

### Información Básica
- **Ubicación**: `/system/priv-app/NetworkDiagnostic/NetworkDiagnostic.apk`
- **Paquete**: `com.samsung.android.networkdiagnostic`
- **Tipo**: Aplicación privilegiada del sistema

### Archivos APK
- `/system/priv-app/NetworkDiagnostic/NetworkDiagnostic.apk`

### Permisos XML
- `/system/etc/permissions/privapp-permissions-com.samsung.android.networkdiagnostic.xml`
  - `com.sec.android.diagmonagent.permission.DIAGMON`
  - `com.sec.android.diagmonagent.permission.PROVIDER`
  - `com.samsung.permission.HQM_NOTIFICATION_PERMISSION`
  - `android.permission.WRITE_SECURE_SETTINGS`
  - `android.permission.READ_PRIVILEGED_PHONE_STATE`

### Configuración del Sistema
- Listado en `/system/etc/apks_count_list.txt`
- Listado en `/system/etc/irremovable_list.txt`
- `/system/etc/init/init.network.rc`

---

## 6. SEMFactoryApp (Aplicación de Fábrica SEM)

### Información Básica
- **Ubicación**: `/system/priv-app/SEMFactoryApp/SEMFactoryApp.apk`
- **Paquete**: `com.sem.factoryapp`
- **Tipo**: Aplicación privilegiada del sistema

### Archivos APK y Optimizaciones
- `/system/priv-app/SEMFactoryApp/SEMFactoryApp.apk`
- `/system/priv-app/SEMFactoryApp/oat/arm64/SEMFactoryApp.odex`
- `/system/priv-app/SEMFactoryApp/oat/arm64/SEMFactoryApp.vdex`

### Permisos XML
- `/system/etc/permissions/privapp-permissions-com.sem.factoryapp.xml`
  - `android.permission.WRITE_SECURE_SETTINGS`
  - `com.samsung.android.security.permission.SAMSUNG_KEYSTORE_PERMISSION`

### Configuración del Sistema
- Listado en `/system/etc/apks_count_list.txt`
- Listado en `/system/etc/irremovable_list.txt`

---

## 7. SmartEpdgTestApp (Aplicación de Prueba Smart ePDG)

### Información Básica
- **Ubicación**: `/system/priv-app/SmartEpdgTestApp/SmartEpdgTestApp.apk`
- **Paquete**: `com.sec.epdgtestapp`
- **Tipo**: Aplicación privilegiada del sistema

### Archivos APK y Optimizaciones
- `/system/priv-app/SmartEpdgTestApp/SmartEpdgTestApp.apk`
- `/system/priv-app/SmartEpdgTestApp/oat/arm64/SmartEpdgTestApp.odex`
- `/system/priv-app/SmartEpdgTestApp/oat/arm64/SmartEpdgTestApp.vdex`

### Permisos XML
- `/system/etc/permissions/privapp-permissions-com.sec.epdgtestapp.xml`
  - `android.permission.CONNECTIVITY_INTERNAL`
  - `android.permission.MODIFY_PHONE_STATE`
  - `android.permission.WRITE_SECURE_SETTINGS`
  - `android.permission.READ_PRIVILEGED_PHONE_STATE`
  - `android.permission.INTERACT_ACROSS_USERS`
- `/system/etc/permissions/privapp-permissions-com.sec.epdg.xml`

### Framework y Librerías
- `/system/framework/EpdgManager.jar`
- `/system/etc/permissions/epdgmanager_library.xml`
- `/system/etc/epdg_apns_conf.xml`

### Configuración del Sistema
- Listado en `/system/etc/apks_count_list.txt`
- Listado en `/system/etc/irremovable_list.txt`

---

## 8. FactoryTestProvider (Proveedor de Pruebas de Fábrica)

### Información Básica
- **Ubicación**: `/system/priv-app/FactoryTestProvider/FactoryTestProvider.apk`
- **Paquete**: `com.samsung.android.providers.factory`
- **Tipo**: Aplicación privilegiada del sistema

### Archivos APK y Optimizaciones
- `/system/priv-app/FactoryTestProvider/FactoryTestProvider.apk`
- `/system/priv-app/FactoryTestProvider/oat/arm64/FactoryTestProvider.odex`
- `/system/priv-app/FactoryTestProvider/oat/arm64/FactoryTestProvider.vdex`

### Permisos XML
- `/system/etc/permissions/privapp-permissions-com.samsung.android.providers.factory.xml`
  - `android.permission.WRITE_MEDIA_STORAGE`
  - `android.permission.WATCH_APPOPS`
  - `android.permission.SET_PROCESS_LIMIT`
  - `com.samsung.android.permission.SEM_MEDIA_CONTENTS`
  - `android.permission.REBOOT`

### Configuración del Sistema
- Listado en `/system/etc/apks_count_list.txt`
- Listado en `/system/etc/irremovable_list.txt`

### Init Services
- `/vendor/etc/init/hw/init.qcom.factory.rc`
  - Services: `fastmmi`, `vendor.mmid`, `mmi_diag`
  - Factory audio test services

### Binarios de Fábrica
- `/vendor/bin/factory.ssc`
- `/vendor/bin/fmfactorytest`
- `/vendor/bin/fmfactorytestserver`
- `/system_ext/bin/mmi` (factory test binary)
- `/system_ext/bin/mmi_diag`

### Factory Key String
- `/system/etc/permissions/privapp-permissions-com.sec.android.app.factorykeystring.xml`

---

## 9. FactoryCameraFB (Cámara de Fábrica)

### Información Básica
- **Ubicación**: `/system/app/FactoryCameraFB/FactoryCameraFB.apk`
- **Tipo**: Aplicación del sistema

### Archivos APK y Optimizaciones
- `/system/app/FactoryCameraFB/FactoryCameraFB.apk`
- `/system/app/FactoryCameraFB/oat/arm64/FactoryCameraFB.odex`
- `/system/app/FactoryCameraFB/oat/arm64/FactoryCameraFB.vdex`

### Configuración del Sistema
- Listado en `/system/etc/apks_count_list.txt`
- Listado en `/system/etc/irremovable_list.txt`

---

## 10. FactoryAirCommandManager (Gestor de Air Command de Fábrica)

### Información Básica
- **Ubicación**: `/system/app/FactoryAirCommandManager/FactoryAirCommandManager.apk`
- **Tipo**: Aplicación del sistema

### Archivos APK y Optimizaciones
- `/system/app/FactoryAirCommandManager/FactoryAirCommandManager.apk`
- `/system/app/FactoryAirCommandManager/oat/arm64/FactoryAirCommandManager.odex`
- `/system/app/FactoryAirCommandManager/oat/arm64/FactoryAirCommandManager.vdex`

### Configuración del Sistema
- Listado en `/system/etc/apks_count_list.txt`
- Listado en `/system/etc/irremovable_list.txt`

---

## 11. UwbTest (Prueba UWB)

### Información Básica
- **Ubicación**: `/system/app/UwbTest/UwbTest.apk`
- **Paquete**: `com.sec.android.app.uwbtest`
- **Tipo**: Aplicación del sistema

### Archivos APK y Optimizaciones
- `/system/app/UwbTest/UwbTest.apk`
- `/system/app/UwbTest/oat/arm64/UwbTest.odex`
- `/system/app/UwbTest/oat/arm64/UwbTest.vdex`

### Permisos XML
- `/system/etc/permissions/privapp-permissions-com.sec.android.app.uwbtest.xml`
  - `android.permission.WRITE_SECURE_SETTINGS`
  - `android.permission.ACCESS_FINE_LOCATION`
  - `android.permission.ACCESS_BACKGROUND_LOCATION`
  - `com.samsung.android.uwb.READ_NOTIFICATION`

### Framework y Librerías
#### Framework JARs
- `/system/framework/semuwb-service.jar`
- `/system/framework/com.samsung.android.uwb_extras.jar`

#### Permission Files
- `/system/etc/permissions/com.samsung.android.uwb_extras.xml`
- `/vendor/etc/permissions/samsung.hardware.uwb.xml`
- `/vendor/etc/permissions/android.hardware.uwb.xml`

#### System Libraries
- `/system/lib/libtflite_uwb_jni.so`
- `/system/lib64/libtflite_uwb_jni.so`

#### Vendor Libraries
- `/vendor/lib64/uwb_uci.hal.so`
- `/vendor/firmware/uwb/libsr200t_prod_fw.so`

### Init Services
- `/system/etc/init/init.system.uwb.rc`
- `/system/etc/init/digitalkey_init_uwb_tss2.rc`
- `/vendor/etc/init/init.vendor.uwb.rc`
- `/vendor/etc/init/vendor.samsung.hardware.uwb@1.0-service.rc`

### UWB Service
- `/vendor/bin/hw/vendor.samsung.hardware.uwb@1.0-service`
- `/vendor/etc/vintf/manifest/vendor.samsung.hardware.uwb@1.0-service.xml`

### Configuración del Sistema
- Listado en `/system/etc/apks_count_list.txt`
- Listado en `/system/etc/irremovable_list.txt`
- `/system/etc/uwb_key` (copied to `/data/uwb/Key` at runtime)

---

## 12. WlanTest (Prueba WLAN)

### Información Básica
- **Ubicación**: `/system/app/WlanTest/WlanTest.apk`
- **Tipo**: Aplicación del sistema

### Archivos APK y Optimizaciones
- `/system/app/WlanTest/WlanTest.apk`
- `/system/app/WlanTest/oat/arm64/WlanTest.odex`
- `/system/app/WlanTest/oat/arm64/WlanTest.vdex`

### Binarios
- `/system/bin/wlandutservice`

### Init Services
- `/vendor/etc/init/init.vendor.wlan.rc`

### Configuración del Sistema
- Listado en `/system/etc/apks_count_list.txt`
- Listado en `/system/etc/irremovable_list.txt`

---

## Dependencias Compartidas (Usadas por Múltiples Apps)

### Data Factory Libraries (Qualcomm)
Usadas por aplicaciones de diagnóstico de red y módem:

#### System_ext Framework JARs
- `vendor.qti.data.factory-V1.0-java.jar` hasta `V2.8-java.jar`
- `vendor.qti.data.factoryservice-V1-java.jar` y `V2-java.jar`
- `vendor.qti.hardware.data.connectionfactory-V1-java.jar`
- `vendor.qti.hardware.data.iwlan-V1.0-java.jar` y `V1.1-java.jar`
- `vendor.qti.hardware.data.iwlandata-V1-java.jar`

#### System_ext Native Libraries (32-bit y 64-bit)
- `vendor.qti.data.factory@*.so` (múltiples versiones)
- `vendor.qti.data.factoryservice-V*-ndk.so`
- `vendor.qti.hardware.data.connectionfactory-V1-ndk.so`
- `vendor.qti.hardware.data.iwlan@*.so`
- `vendor.qti.hardware.data.iwlandata-V1-ndk.so`

#### Vendor Native Libraries
- `vendor.qti.data.factory@*.so` (múltiples versiones en `/vendor/lib` y `/vendor/lib64`)
- `vendor.qti.hardware.data.connectionfactory-V1-ndk.so`
- `libnetmgrmodemproxy.so`
- `vendor.samsung.hardware.radio.network-V1-ndk.so`

### IMS Factory Libraries (Qualcomm)
Usadas para diagnósticos de telefonía y comunicaciones:

#### System_ext Framework JARs
- `vendor.qti.ims.factory-V1.0-java.jar` hasta `V2.2-java.jar`
- `vendor.qti.ims.factoryaidlservice-V1-java.jar`

#### System_ext Native Libraries
- `vendor.qti.ims.factory@*.so` (múltiples versiones)
- `vendor.qti.ims.factoryaidlservice-V1-ndk.so`

### Samsung Bitmap Factory
- `/system/lib/libsembitmapfactory_jni.so`
- `/system/lib64/libsembitmapfactory_jni.so`

---

## Resumen de Tipos de Dependencias

### 1. Archivos APK
Todos los APKs están ubicados en:
- `/system/priv-app/` (aplicaciones privilegiadas)
- `/system/app/` (aplicaciones del sistema)

### 2. Archivos de Optimización
Para cada APK:
- `.odex` - Código optimizado
- `.vdex` - Datos de verificación

### 3. Permisos XML
Ubicados en `/system/etc/permissions/`:
- `privapp-permissions-*.xml` - Permisos privilegiados para apps
- `*.xml` - Permisos y librerías del sistema

### 4. Framework JARs
Ubicados en:
- `/system/framework/` - Framework del sistema
- `/system_ext/framework/` - Framework extendido (Qualcomm)

### 5. Librerías Nativas (.so)
Ubicadas en:
- `/system/lib/` y `/system/lib64/`
- `/system_ext/lib/` y `/system_ext/lib64/`
- `/vendor/lib/` y `/vendor/lib64/`

### 6. Binarios Ejecutables
Ubicados en:
- `/system/bin/`
- `/vendor/bin/`
- `/system_ext/bin/`

### 7. Init Services (RC Files)
Ubicados en:
- `/system/etc/init/`
- `/vendor/etc/init/`
- `/vendor/etc/init/hw/`

### 8. Configuración del Sistema
- `/system/etc/apks_count_list.txt` - Lista de conteo de APKs
- `/system/etc/irremovable_list.txt` - Lista de apps irremovibles
- Archivos de configuración específicos en `/system/etc/`

### 9. Contextos SELinux
Todos los archivos del sistema tienen contextos SELinux definidos en:
- `file_context-system` - Contextos para partición system
- `file_context-vendor` - Contextos para partición vendor
- Contexto principal: `u:object_r:system_file:s0`

---

## Notas Importantes

1. **Apps Irremovibles**: Todas estas aplicaciones están listadas en `irremovable_list.txt`, lo que significa que el sistema las protege contra la eliminación.

2. **Permisos Privilegiados**: Las apps en `/priv-app/` tienen acceso a permisos especiales del sistema definidos en archivos XML de permisos.

3. **Optimización ART**: Todos los APKs tienen archivos `.odex` y `.vdex` precompilados para optimizar el rendimiento.

4. **Dependencias de Qualcomm**: Muchas de estas apps dependen de librerías y servicios de Qualcomm, especialmente para funciones de diagnóstico y fábrica.

5. **Servicios de Sistema**: Varias apps requieren servicios de sistema que se inician mediante archivos `.rc` en el arranque del dispositivo.

6. **Modo de Fábrica**: El archivo `init.qcom.factory.rc` define el comportamiento del sistema en modo de fábrica (FFBM/QMMI).
