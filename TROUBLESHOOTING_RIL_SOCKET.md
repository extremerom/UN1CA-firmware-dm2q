# 🔧 Troubleshooting: Socket RIL No Encontrado y Métodos Alternativos

## 📋 Problema: Socket `/dev/socket/rild` No Existe

### Diagnóstico del Problema

Si el comando `ls /dev/socket/` no muestra `rild`, esto puede deberse a:

1. **Arquitectura diferente del RIL** en tu dispositivo
2. **Samsung Knox está bloqueando** el acceso
3. **Socket con nombre diferente** en tu ROM/firmware
4. **Servicio RIL no iniciado** o usando otra implementación

---

## 🔍 Paso 1: Identificar el Socket RIL Correcto

### Buscar Sockets Relacionados con RIL

```bash
# Método 1: Buscar sockets de radio/telephony
ls -la /dev/socket/ | grep -iE "ril|radio|qmux|telephony"

# Método 2: Buscar procesos relacionados
ps -A | grep -iE "ril|radio|telephony|modem"

# Método 3: Buscar en propiedades del sistema
getprop | grep -iE "ril|radio"

# Método 4: Verificar servicios activos
service list | grep -iE "phone|radio|ril"
```

**En tu caso**, veo que tienes:
- `qmux_radio/` - Este es probablemente tu socket de comunicación con el modem
- `location/` - Puede contener sockets relacionados
- Varios sockets de Qualcomm (`qcc_trd/`, `qsap_location/`)

---

## 🔌 Paso 2: Métodos Alternativos para Ejecutar Comandos AT

### Método 1: Via QMI (Qualcomm MSM Interface)

El socket `qmux_radio/` sugiere que tu dispositivo usa QMI en lugar de AT commands directos.

```bash
# Listar sockets dentro de qmux_radio
ls -la /dev/socket/qmux_radio/

# Ejemplo de conexión (necesita adaptación)
# QMI usa un protocolo binario diferente a AT commands
```

**Nota**: QMI requiere herramientas especiales como `qmicli` o `libqmi`.

### Método 2: Via Service Call (Telephony Manager)

```bash
# Obtener servicio de teléfono
service call phone 1

# Listar métodos disponibles
service list | grep phone

# Ejemplo de uso (varía según dispositivo)
service call phone 2 s16 "AT+CFUN?"
```

### Método 3: Via ATFWD-daemon

Algunos dispositivos Samsung usan un daemon especializado:

```bash
# Verificar si existe
ps -A | grep atfwd

# Si existe, intentar conectar a su socket
# (buscar el socket específico en /dev/socket/)
```

### Método 4: Via Aplicación de Sistema (ModemServiceMode)

```bash
# Activar menú de servicio directamente
am start -n com.sec.android.RilServiceModeApp/.ServiceModeApp \
  --es keyString "0011"

# Ver logs de comandos AT
logcat -s RILJ:V RIL:V ModemServiceMode:V
```

### Método 5: Via Content Provider (Si disponible)

```bash
# Algunos dispositivos exponen comandos AT via content provider
content query --uri content://com.android.internal.telephony/carriers

# O directamente via settings
settings get system telephony_at_commands
```

---

## 🔧 Paso 3: Instalar Herramientas QMI

Si tu dispositivo usa QMI (Qualcomm), necesitas herramientas especiales:

### Instalación de libqmi y qmicli

```bash
# En Termux
pkg install libqmi qmicli

# Verificar instalación
qmicli --version

# Listar dispositivos
qmicli -d /dev/cdc-wdm0 --get-service-version-info

# O buscar el dispositivo correcto
ls -la /dev/ | grep -E "cdc|qmi|wwan"
```

### Usar qmicli para comandos básicos

```bash
# Obtener info del modem
qmicli -d /dev/cdc-wdm0 --dms-get-manufacturer
qmicli -d /dev/cdc-wdm0 --dms-get-model
qmicli -d /dev/cdc-wdm0 --dms-get-revision

# Estado de red
qmicli -d /dev/cdc-wdm0 --nas-get-signal-strength
qmicli -d /dev/cdc-wdm0 --nas-get-serving-system

# Info de SIM
qmicli -d /dev/cdc-wdm0 --uim-get-card-status
```

---

## 📱 Paso 4: Métodos Específicos para Samsung Knox

### ¿Por Qué Knox Puede Estar Bloqueando?

Samsung Knox implementa varias capas de seguridad:

1. **SELinux policies** - Bloquean acceso a sockets sensibles
2. **Knox Container** - Aísla procesos del sistema
3. **Real-Time Kernel Protection (RKP)** - Monitorea llamadas al sistema
4. **Trusted Boot** - Verifica integridad del sistema

### Verificar Estado de Knox

```bash
# Verificar si Knox está activo
getprop ro.boot.warranty_bit
getprop ro.boot.verifiedbootstate
getprop ro.build.selinux

# Ver políticas SELinux
getenforce
sestatus

# Verificar contextos de seguridad
ls -Z /dev/socket/
```

### Desactivar Knox (⚠️ Puede Invalidar Garantía)

```bash
# Método 1: Via Magisk (si está instalado)
# Instalar módulo "Knox Patcher" desde Magisk Manager

# Método 2: Modificar políticas SELinux (temporal)
setenforce 0  # Permissive mode

# Método 3: Desactivar servicios Knox
pm disable com.samsung.android.knox.analytics.uploader
pm disable com.samsung.android.knox.attestation
pm disable com.samsung.android.knox.containeragent
```

---

## 🔐 Paso 5: Soluciones Alternativas sin Socket RIL

### Opción A: Usar API de Telephony Manager

```java
// Código Java/Kotlin para app Android
import android.telephony.TelephonyManager;
import android.content.Context;

TelephonyManager tm = (TelephonyManager) context.getSystemService(Context.TELEPHONY_SERVICE);

// Métodos disponibles sin necesidad de socket
String imei = tm.getImei();
String operator = tm.getNetworkOperatorName();
int signalStrength = tm.getSignalStrength();
```

### Opción B: Usar ModemServiceMode App

```bash
# Activar diferentes menús
am start -n com.sec.android.RilServiceModeApp/.ServiceModeApp --es keyString "0011"
am start -n com.sec.android.RilServiceModeApp/.ServiceModeApp --es keyString "9900"
am start -n com.sec.android.RilServiceModeApp/.ServiceModeApp --es keyString "2663"
```

### Opción C: Network Signal Guru (App)

Si tienes root:
1. Instalar Network Signal Guru desde Play Store
2. Otorgar permisos root
3. La app puede enviar comandos AT internamente

---

## 🔎 Paso 6: Encontrar el Socket Correcto en Tu Dispositivo

### Script de Búsqueda Automática

```bash
#!/system/bin/sh
# find_ril_socket.sh

echo "=== Buscando socket RIL ==="

# Buscar sockets con nombres relacionados
echo "Sockets en /dev/socket/:"
ls -la /dev/socket/ | grep -iE "ril|radio|qmux|phone|telephony|modem"

echo ""
echo "=== Procesos relacionados ==="
ps -A | grep -iE "ril|radio|telephony"

echo ""
echo "=== Propiedades del sistema ==="
getprop | grep -iE "rild|ril\." | head -20

echo ""
echo "=== Servicios activos ==="
service list | grep -iE "phone|radio|ril"

echo ""
echo "=== Dispositivos QMI ==="
ls -la /dev/ | grep -E "cdc|qmi|wwan|rmnet"

echo ""
echo "=== Sockets en qmux_radio ==="
if [ -d "/dev/socket/qmux_radio" ]; then
    ls -la /dev/socket/qmux_radio/
fi
```

**Guardar y ejecutar**:
```bash
adb push find_ril_socket.sh /data/local/tmp/
adb shell su -c "chmod +x /data/local/tmp/find_ril_socket.sh"
adb shell su -c "/data/local/tmp/find_ril_socket.sh"
```

---

## 📊 Paso 7: Solución Específica para Tu Dispositivo

Basado en tu output de `ls /dev/socket/`, tu dispositivo tiene:

### Sockets Disponibles en Tu Sistema

```
qmux_radio/           ← ESTE ES PROBABLEMENTE TU SOCKET RIL
location/
qcc_trd/
qsap_location/
```

### Intentar Conexión a qmux_radio

```bash
# Listar contenido
ls -la /dev/socket/qmux_radio/

# Si hay sockets dentro, intentar conexión
# Ejemplo (el nombre exacto puede variar):
echo -e "AT\r\n" | nc -U /dev/socket/qmux_radio/qmux_connect_socket
```

### Usar Herramientas Qualcomm

```bash
# Si qmux_radio existe, probablemente necesitas herramientas QMI
# Instalar en Termux:
pkg install libqmi

# Buscar dispositivo QMI
ls -la /dev/ | grep qmi

# Ejemplo de uso
qmicli -d /dev/qmi0 --dms-get-manufacturer
```

---

## 🛠️ Paso 8: Crear Socket RIL Manualmente (Avanzado)

⚠️ **MUY PELIGROSO** - Solo para expertos

```bash
# Verificar que rild no está corriendo
ps -A | grep rild

# Iniciar rild manualmente (puede causar problemas)
# NO EJECUTAR A MENOS QUE SEPAS LO QUE HACES
# rild -l /vendor/lib64/libsec-ril.so

# O reiniciar el servicio
# stop ril-daemon
# start ril-daemon
```

---

## 📱 Paso 9: Métodos de Diagnóstico Alternativos

### Usar Códigos USSD/MMI

Estos funcionan sin necesidad de acceso al socket:

```bash
# Desde el marcador telefónico
*#06#          # IMEI
*#0*#          # Menú de pruebas
*#0011#        # Service mode
*#9900#        # SysDump
*#2663#        # TSP firmware
*#0228#        # Batería
```

### Usar ADB para Información

```bash
# Info del dispositivo
adb shell getprop ro.build.fingerprint
adb shell getprop gsm.version.baseband

# Logs de telephony
adb logcat -b radio

# Dump de estado
adb shell dumpsys telephony.registry
adb shell dumpsys phone
```

---

## 🔐 Análisis de Knox y Alternativas

### Por Qué Knox Interfiere

Samsung Knox implementa:

1. **TrustZone** - Procesador seguro aislado
2. **TIMA (TrustZone-based Integrity Measurement Architecture)**
3. **Real-time Kernel Protection (RKP)**
4. **Secure Boot**
5. **DM-Verity** - Verificación de particiones

### Verificar Si Knox Te Está Bloqueando

```bash
# Ver logs de Knox
logcat -s KNOX:V

# Verificar contador Knox
getprop ro.boot.warranty_bit
# 0 = No tripped, 1 = Tripped (warranty void)

# Ver estado de knox
getprop ro.boot.vbmeta.device_state
```

### Bypass de Knox (Si Es Necesario)

```bash
# Opción 1: Custom ROM sin Knox
# - LineageOS
# - Pixel Experience
# - etc.

# Opción 2: Magisk con módulos
# - Universal SafetyNet Fix
# - Knox Patcher
# - SELinux Permissive

# Opción 3: Desactivar verificación (temporal)
setenforce 0
```

---

## 📝 Conclusión y Recomendaciones

### Para Tu Caso Específico

1. **Tu dispositivo usa QMI**, no AT commands directos
2. **Instalar libqmi/qmicli** para comunicación con modem
3. **Usar ModemServiceMode** para menús de servicio
4. **Knox puede estar bloqueando** acceso a sockets

### Próximos Pasos Recomendados

```bash
# 1. Explorar qmux_radio
ls -laR /dev/socket/qmux_radio/

# 2. Instalar herramientas QMI
pkg install libqmi qmicli

# 3. Buscar dispositivo QMI
ls -la /dev/ | grep -E "qmi|cdc|wwan"

# 4. Usar ModemServiceMode para funcionalidad básica
am start -n com.sec.android.RilServiceModeApp/.ServiceModeApp --es keyString "0011"

# 5. Capturar logs para análisis
logcat -b radio -v time > /sdcard/radio_log.txt
```

---

## 🆘 Si Nada Funciona

### Plan B: Usar Aplicaciones de Sistema

```bash
# SecFactoryPhoneTest
am start -n com.sec.phone/.SecPhoneService

# TelephonyUI
am start -n com.android.phone/.TelephonyUI

# DeviceDiagnostics
am start -n com.sec.android.app.servicemodeapp/.DeviceDiagnostics
```

### Plan C: Análisis con Herramientas Externas

1. **QPST (Qualcomm Product Support Tools)** - Desde PC con cable USB
2. **QXDM (Qualcomm eXtensible Diagnostic Monitor)** - Análisis avanzado
3. **Network Signal Guru** - App con root para comandos AT

---

## ⚠️ Advertencia Final

- **NO intentes crear sockets manualmente** sin conocimiento experto
- **Hacer backup de EFS** antes de cualquier experimento
- **Knox tripped = Garantía perdida**
- **Algunos cambios son irreversibles**

---

**Documentación creada**: Diciembre 2024  
**Dispositivo**: Samsung Galaxy S23 (SM-S916B / r0q según tu output)  
**Problema**: Socket RIL no disponible, dispositivo usa QMI

Ver también:
- AT_COMMANDS_EXECUTION_GUIDE.md - Métodos generales
- EXTENDED_AT_COMMANDS_ANALYSIS.md - Comandos documentados
- KNOX_ANALYSIS.md - Análisis específico de Knox (próximo documento)
