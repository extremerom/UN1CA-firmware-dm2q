# Funcionalidades Ocultas - Análisis Detallado Técnico

## 1. Servicios de Diagnóstico Ocultos

### 1.1 Servicios Activos en Init Scripts

#### Servicio de Diagnóstico Principal
```rc
service vendor.diag-router /vendor/bin/diag-router
    class hal
    user system
    group system
    capabilities KILL
    disabled
```

**Función**: Enrutador de diagnóstico Qualcomm que permite:
- Comunicación con el modem
- Acceso a logs del sistema
- Interface con herramientas QXDM/QPST

#### CoreSight Tracing (Depuración de Hardware)

El sistema configura múltiples dispositivos CoreSight para tracing a nivel de hardware:

```rc
on early-boot
    chown system system /sys/bus/coresight/devices/coresight-tmc-etf/curr_sink
    chown system system /sys/bus/coresight/devices/coresight-tmc-etf/enable_sink
    chown system system /sys/bus/coresight/devices/coresight-tmc-etr/curr_sink
    chown system system /sys/bus/coresight/devices/coresight-stm/enable
    chown system system /sys/bus/coresight/devices/coresight-modem-diag/enable_source
```

**Capacidades**:
- **TMC-ETF**: Trace Memory Controller - Embedded Trace FIFO
- **TMC-ETR**: Trace Memory Controller - Embedded Trace Router
- **STM**: System Trace Macrocell
- **TPIU**: Trace Port Interface Unit
- **Hardware Event Tracing**: Trazado de eventos del modem

### 1.2 Servicios de Diagnóstico Completos

| Servicio | Binario | Función |
|----------|---------|---------|
| sec_diag_uart_log | /system/bin/sec_diag_uart_log | Logging UART Samsung |
| vendor.diag-router | /vendor/bin/diag-router | Router principal de diagnóstico |
| vendor.ipacm-diag | /system/vendor/bin/ipacm-diag | Diagnóstico IPA |
| vendor.cnss_diag | /system/vendor/bin/cnss_diag | Diagnóstico de conectividad |
| vendor.ssr_diag | /system/vendor/bin/ssr_diag | Subsystem Restart diagnosis |
| diag_mdlog_start | /system/vendor/bin/diag_mdlog | Logging del modem |
| mmi_diag | /system_ext/bin/mmi_diag | MMI diagnostic interface |
| factory_ssc | /vendor/bin/factory.ssc | Factory Sensor Core tests |

## 2. Análisis de Aplicaciones Ocultas

### 2.1 SmartTutor - Soporte Remoto Oculto

**Ubicación**: `/system/system/hidden/SmartTutor/SmartTutor.apk`
**Tamaño**: 24.5 MB
**Estado**: Oculto pero instalado

#### Características probables:
- Acceso remoto al dispositivo
- Diagnóstico remoto por técnicos Samsung
- Control remoto de pantalla
- Acceso a logs del sistema
- Posible back-door legítimo para soporte técnico

#### Cómo podría activarse:
```bash
# Posibles métodos de activación
am start -n com.samsung.smarttutor/.MainActivity
# O mediante código secreto en el dialer
```

### 2.2 FactoryTestProvider

**Package**: `com.sec.factory`
**Ubicación**: `/system/system/priv-app/FactoryTestProvider/`
**Privilegios**: PRIVILEGED (acceso sistema completo)

#### Funcionalidades expuestas:
- Content Provider para tests de fábrica
- Acceso a hardware de bajo nivel
- APIs para calibración de sensores
- Tests de producción

### 2.3 SecFactoryPhoneTest

**Package**: `com.sec.factory.phone`
**Ubicación**: `/system/system/priv-app/SecFactoryPhoneTest/`

#### Tests disponibles (típicos):
- Test de pantalla táctil
- Test de botones físicos
- Test de altavoces/micrófono
- Test de vibración
- Test de sensores (acelerómetro, giroscopio, proximidad)
- Test de cámara frontal y trasera
- Test de flash LED
- Test de conectividad (WiFi, Bluetooth, NFC, GPS)
- Test de carga
- Test de batería

#### Código secreto probable: `*#0*#`

### 2.4 DiagMonAgent95

**Package**: `com.sec.android.diagmonagent`
**Ubicación**: `/system/system/priv-app/DiagMonAgent95/`
**Versión**: 95 (indica versión muy reciente)

#### Funcionalidad de Monitoreo:
- Recolección de logs del sistema
- Monitoreo de crashes
- Análisis de performance
- Telemetría a servidores Samsung
- Diagnóstico automático de problemas

**Posible privacidad**: Este agente puede enviar información del dispositivo a Samsung.

## 3. Módulos del Kernel para Dump y Debugging

### 3.1 Módulos de Recolección de Dumps

#### qcom_ramdump.ko
```
Función: Captura completa de la RAM en caso de crash
Uso: Análisis post-mortem de kernel panics
Ubicación de dumps: /data/vendor/ramdump/
```

#### qcom_va_minidump.ko
```
Función: Mini dumps optimizados para análisis de vulnerabilidades
Tamaño: Reducido para transmisión rápida
Uso: Debugging remoto y análisis de seguridad
```

#### microdump_collector.ko
```
Función: Recolección de micro dumps del sistema
Información: Stack traces, registros del CPU, estado mínimo
Ventaja: Overhead mínimo en producción
```

#### dmesg_dumper.ko
```
Función: Captura automática de dmesg en crashes
Persistencia: Survives reboots
Ubicación: Partition especial o /data
```

#### sec_tsp_dumpkey.ko
```
Función: Dump key del touchscreen Samsung
Uso: Debugging de problemas táctiles
Activación: Combinación de botones especial
```

### 3.2 Cómo Acceder a los Dumps (si tienes root)

```bash
# Listar dumps disponibles
ls -la /data/vendor/ramdump/
ls -la /data/vendor/tombstones/
ls -la /data/vendor/ssrdump/

# Ver último dmesg guardado
cat /sys/fs/pstore/console-ramoops-0

# Acceder a mini dumps
cat /sys/fs/pstore/dmesg-ramoops-*
```

## 4. Interface de Diagnóstico Qualcomm

### 4.1 Protocolo DIAG

El firmware incluye soporte completo para el protocolo DIAG de Qualcomm:

**Puerto USB**: Típicamente expuesto como `/dev/diag`
**Herramientas compatibles**:
- QXDM (Qualcomm eXtensible Diagnostic Monitor)
- QPST (Qualcomm Product Support Tools)
- DFS (Diag Frame Sender)

### 4.2 Comandos DIAG Disponibles

El sistema expone las siguientes capacidades via DIAG:

```
- Lectura/escritura NV items
- Acceso a logs del modem
- Comandos AT al modem
- Logs de eventos del sistema
- Información de RF (Radio Frequency)
- Estadísticas de red
- Información de SIM/USIM
```

### 4.3 Activación del Puerto DIAG

**Método 1 - ADB (requiere desarrollo habilitado)**:
```bash
adb shell
su
setprop sys.usb.config diag,adb
```

**Método 2 - Código secreto** (algunos dispositivos):
```
*#9090#  # USB settings
*#0808#  # USB configuration
```

### 4.4 Librerías DIAG

```
vendor/lib/libdiag.so
vendor/lib/libdiagjni.so
vendor/lib/vendor.qti.diaghal@1.0.so
```

**API disponible**:
- Interface JNI para apps Android
- HAL para servicios del sistema
- Interface nativa para binarios

## 5. Sistema Knox - Análisis de Seguridad

### 5.1 Knox Matrix

```properties
ro.security.knoxmatrix=true
```

**Knox Matrix**: Nueva característica de seguridad cross-device
- Autenticación entre dispositivos Samsung
- Sincronización segura de credenciales
- Protección de dispositivos conectados

### 5.2 Componentes Knox Instalados

#### SDK Principal
```
/system/system/framework/knoxsdk.jar
```
**API Level**: 39
**Capacidades**:
- MDM (Mobile Device Management)
- Container seguro (Knox Workspace)
- VPN per-app
- App firewall
- Cifrado de archivos
- Sandboxing avanzado

#### Knox Analytics
```
/system/system/framework/knoxanalyticssdk.jar
```
**Función**: Recolección de eventos de seguridad
**Datos monitoreados**:
- Intentos de root
- Instalación de apps sospechosas
- Modificaciones del sistema
- Violaciones de políticas

#### Knox MTD (Mobile Threat Defense)
```
/system/system/framework/knox_mtd.jar
```
**Protecciones**:
- Anti-malware en tiempo real
- Detección de apps maliciosas
- Análisis de permisos
- Protección contra phishing

### 5.3 Librerías Nativas Knox

```c
// libknoxnative_shared.so - Funciones principales
knox_verify_boot()
knox_check_integrity()
knox_secure_storage_access()
knox_enforce_policy()

// libknox_filemanager.so - Gestión de archivos
knox_encrypt_file()
knox_decrypt_file()
knox_secure_delete()
```

### 5.4 Permisos Knox Privilegiados

Apps con acceso a Knox APIs:
- `com.samsung.android.knox.*` - Apps sistema Knox
- `com.sec.enterprise.knox.*` - Enterprise Knox
- `com.samsung.android.knox.mpos` - Mobile POS
- `com.samsung.android.knox.attestation` - Attestation

## 6. Códigos Secretos Confirmados

### 6.1 Sistema de Broadcast

```xml
<allow-implicit-broadcast action="android.telephony.action.SECRET_CODE" />
```

El sistema permite broadcasts implícitos para códigos secretos, lo que significa que apps privilegiadas pueden registrar receivers para:

```java
<receiver android:name=".SecretCodeReceiver">
    <intent-filter>
        <action android:name="android.telephony.action.SECRET_CODE" />
        <data android:scheme="android_secret_code" android:host="código" />
    </intent-filter>
</receiver>
```

### 6.2 Códigos Probables (requieren verificación en dispositivo)

| Código | Función Esperada | App Objetivo |
|--------|------------------|--------------|
| `*#0*#` | General hardware test | SecFactoryPhoneTest |
| `*#0228#` | Battery status | Battery test app |
| `*#12580*369#` | SW & HW info | System info |
| `*#9900#` | SysDump mode | Diagnostic tool |
| `*#0808#` | USB settings | USB configuration |
| `*#2663#` | TSP firmware version | Touchscreen info |
| `*#0011#` | Service mode | Network info |

### 6.3 Descubrir Códigos Activos

```bash
# Mediante ADB y grep en APKs decompilados
adb pull /system/system/priv-app/SecFactoryPhoneTest/SecFactoryPhoneTest.apk
apktool d SecFactoryPhoneTest.apk
grep -r "android_secret_code" SecFactoryPhoneTest/
```

## 7. Características Avanzadas de Cámara

### 7.1 Librerías IA de Procesamiento

#### Beauty Mode v4
```
/vendor/lib/libBeauty_v4.camera.samsung.so
```
**Funcionalidades**:
- Suavizado de piel multinivel
- Ajuste de tono de piel
- Reducción de imperfecciones
- Ajuste de rasgos faciales (ojos, nariz)

#### AI Multi Frame ISP
```
/vendor/lib/libAIMFISP.camera.samsung.so
```
**Capacidades**:
- Fusión de múltiples frames con IA
- Reducción de ruido inteligente
- HDR computacional
- Super resolución

#### Light Object Detector
```
/vendor/lib/libLightObjectDetector_v1.camera.samsung.so
```
**Detección**:
- Reconocimiento de objetos
- Optimización de parámetros por escena
- Detección de rostros avanzada
- Tracking de objetos

#### OpenCV Integration
```
/vendor/lib/libOpenCv.camera.samsung.so
```
**Algoritmos**:
- Visión por computadora
- Detección de bordes
- Transformaciones geométricas
- Filtros avanzados

### 7.2 Captura Personal
```
/vendor/lib/libPersonal_capture.camera.samsung.so
```
**Función**: Personalización de procesamiento de imagen
- Perfiles de usuario
- Preferencias de procesamiento
- Estilos personalizados

### 7.3 Face Analysis
```
/vendor/lib/libHprFace_GAE_api.camera.samsung.so
```
**HPR Face**: High Performance Recognition
**GAE**: Geometric Alignment Engine

**Capacidades**:
- Reconocimiento facial rápido
- Alineación precisa de rasgos
- Análisis de expresiones
- Age/gender estimation

## 8. Capacidades de Blockchain

### 8.1 Hardware Blockchain Support

```
/vendor/lib/vendor.samsung.hardware.tlc.blockchain@1.0.so
```

**TLC**: Trusted Logic Client (anteriormente Trustonic)

**Funcionalidades**:
- Wallet seguro a nivel de hardware
- Firma de transacciones en TrustZone
- Almacenamiento seguro de claves privadas
- APIs para apps blockchain

### 8.2 Aplicaciones Potenciales

- Samsung Blockchain Keystore
- Cryptocurrency wallets
- DApp (Decentralized Applications)
- Firma digital de documentos

## 9. Conectividad UWB (Ultra-Wideband)

### 9.1 UwbTest App

**Ubicación**: `/system/system/app/UwbTest/UwbTest.apk`

**Funcionalidades UWB**:
- Posicionamiento de precisión centimétrica
- Car keys digitales
- Smart home automation
- File sharing de proximidad
- Gaming multijugador local

### 9.2 Casos de Uso

- **SmartThings Find**: Localización precisa de dispositivos
- **Digital Car Key**: Desbloqueo de vehículos
- **Nearby Share**: Transferencia rápida de archivos

## 10. Audio Avanzado

### 10.1 Sound Booster Plus

```
/vendor/lib/soundfx/libsamsungSoundbooster_plus.so
```

**Mejoras**:
- Amplificación inteligente
- Ecualización adaptativa
- Expansión de campo sonoro

### 10.2 Audio SA Plus

```
/vendor/lib/soundfx/libaudiosaplus_sec.so
```

**Spatial Audio**:
- Audio 3D
- Head tracking (con Galaxy Buds)
- Virtualización de surround

## 11. Técnicas de Activación de Funciones Ocultas

### 11.1 Mediante ADB

```bash
# Listar todas las activities
adb shell pm list packages -f | grep -i test

# Iniciar SmartTutor oculto
adb shell am start -n com.samsung.smarttutor/.MainActivity

# Iniciar factory test
adb shell am start -n com.sec.factory/.PhoneTestActivity

# Habilitar diagnóstico
adb shell setprop persist.vendor.diag.enable 1
```

### 11.2 Mediante Intent Broadcasts

```bash
# Enviar código secreto manualmente
adb shell am broadcast -a android.telephony.action.SECRET_CODE -d android_secret_code://0000

# Activar diagnostic mode
adb shell am broadcast -a com.sec.android.diagmonagent.intent.USE_APP
```

### 11.3 Mediante Edición de Props (requiere root)

```bash
# Habilitar debugging
setprop ro.debuggable 1
setprop persist.sys.usb.config diag,adb

# Habilitar logging extendido
setprop persist.vendor.verbose_logging 1
```

## 12. Análisis Forense y Seguridad

### 12.1 Ubicaciones de Logs

```bash
# Logs principales
/data/log/
/data/vendor/log/
/data/vendor/ramdump/
/data/vendor/tombstones/
/data/vendor/ssrdump/

# Persistent storage
/sys/fs/pstore/
```

### 12.2 Información de Seguridad

```bash
# Knox status
getprop ro.security.knoxmatrix

# SELinux status
getenforce

# Verificación de boot
getprop ro.boot.verifiedbootstate

# Warranty bit
getprop ro.boot.warranty_bit
```

### 12.3 Extracción de APKs para Análisis

```bash
# Extraer todas las apps de test
adb pull /system/system/app/UwbTest/UwbTest.apk
adb pull /system/system/app/WlanTest/WlanTest.apk
adb pull /system/system/priv-app/SecFactoryPhoneTest/SecFactoryPhoneTest.apk

# Extraer SmartTutor oculto
adb pull /system/system/hidden/SmartTutor/SmartTutor.apk
```

## 13. Vectores de Investigación Adicional

### 13.1 Análisis Binario

```bash
# Analizar binarios de diagnóstico
file /vendor/bin/diag-router
strings /vendor/bin/diag-router | grep -i password
ltrace /vendor/bin/diag-router

# Desempaquetar librerías
adb pull /vendor/lib/libdiag.so
# Analizar con Ghidra/IDA
```

### 13.2 Sniffing de Comunicaciones

```bash
# Capturar tráfico USB
usbmon en Linux

# Capturar logs DIAG
QXDM Professional
# O herramientas open source como:
# - pydiag
# - scat (Samsung Cellular Analysis Tool)
```

### 13.3 Hooking Runtime

```javascript
// Frida script para hooking de Knox
Java.perform(function() {
    var Knox = Java.use("com.samsung.android.knox.SemPersonaManager");
    Knox.getKnoxStatus.implementation = function() {
        console.log("Knox status checked");
        return this.getKnoxStatus();
    };
});
```

## 14. Consideraciones de Seguridad y Legalidad

### ⚠️ ADVERTENCIAS IMPORTANTES

1. **Modificación del Sistema**: 
   - Invalidará la garantía
   - Activará Knox e-fuse (permanente)
   - Puede causar brick del dispositivo

2. **Legalidad**:
   - Uso de herramientas de diagnóstico puede violar términos de servicio
   - Acceso a funciones ocultas puede violar regulaciones
   - Compartir dumps puede violar NDAs

3. **Privacidad**:
   - Herramientas de diagnóstico pueden exponer datos personales
   - Logs pueden contener información sensible
   - DiagMonAgent envía telemetría a Samsung

4. **Seguridad**:
   - No deshabilitar Knox sin entender consecuencias
   - Mantener SELinux en enforcing
   - No exponer puerto DIAG en redes públicas

---

**Documento técnico**: Análisis de funcionalidades ocultas
**Fecha**: 2025-12-28
**Dispositivo**: Samsung Galaxy S23 (SM-S916B)
**Firmware**: S916BXXS8EYK5
**Propósito**: Investigación y educación
