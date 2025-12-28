# Ejemplos Prácticos de Uso - Funcionalidades Descubiertas

## 🎯 Guía de Aplicación Práctica

Este documento proporciona ejemplos prácticos de cómo utilizar las funcionalidades ocultas descubiertas en el análisis de ingeniería inversa del firmware Samsung Galaxy S23.

## 1. Activación de SmartTutor (Soporte Remoto)

### Método 1: Via ADB

```bash
# Conectar el dispositivo con USB debugging habilitado
adb devices

# Iniciar SmartTutor
adb shell am start -n com.samsung.smarttutor/.MainActivity

# Alternativa: Iniciar con intent específico
adb shell am start -a android.intent.action.MAIN \
  -n com.samsung.smarttutor/.MainActivity
```

### Método 2: Via Activity Manager (en dispositivo)

```bash
# En terminal del dispositivo (requiere adb shell o terminal app)
am start -n com.samsung.smarttutor/.MainActivity
```

### Qué esperar:
- Pantalla de inicio de SmartTutor
- Opciones de conexión remota
- Puede requerir permisos adicionales
- Interfaz de soporte técnico Samsung

## 2. Acceso a Tests de Fábrica

### Test Completo de Hardware (*#0*#)

**Procedimiento**:
1. Abrir la aplicación de teléfono (dialer)
2. Ingresar: `*#0*#`
3. Se abrirá el menú de test automáticamente

**Tests disponibles**:
- LCD Display (colores RGB, negro, blanco)
- Touch screen (dibuja para verificar)
- Speaker/Receiver test
- Vibration test
- Camera (frontal y trasera)
- Sensor test (acelerómetro, giroscopio, proximidad, luz)
- LED test (flash)

### Test de Batería

```bash
# Via código secreto (si disponible)
# Marcar: *#0228#

# Via ADB
adb shell dumpsys battery
adb shell cat /sys/class/power_supply/battery/capacity
adb shell cat /sys/class/power_supply/battery/health
adb shell cat /sys/class/power_supply/battery/temp
```

### Test de Conectividad

```bash
# Iniciar test de WiFi
adb shell am start -n com.sec.android.app.wlantest/.WlanTest

# Iniciar test de UWB
adb shell am start -n com.sec.android.app.uwbtest/.UWBTest

# Información de WiFi
adb shell dumpsys wifi

# Información de Bluetooth
adb shell dumpsys bluetooth_manager
```

## 3. Diagnóstico de Red y Conectividad

### Información Detallada de Red

```bash
# Service mode - Info de señal
# Código: *#0011#

# Via ADB - Status de red
adb shell dumpsys telephony.registry

# Info de SIM
adb shell dumpsys isub

# Estado de datos móviles
adb shell dumpsys connectivity

# Ver APNs configurados
adb shell content query --uri content://telephony/carriers
```

### Test de VoLTE/VoWiFi

```bash
# Iniciar SmartEpdgTestApp
adb shell pm list packages | grep epdg
adb shell am start -n com.sec.epdg/.SmartEpdgTestActivity
```

## 4. Acceso a Logs del Sistema

### Logs Estándar

```bash
# Logcat en tiempo real
adb logcat

# Logcat filtrado por tag
adb logcat -s DiagMonAgent
adb logcat -s Knox
adb logcat -s Camera

# Guardar logs
adb logcat -d > logcat_$(date +%Y%m%d_%H%M%S).txt

# Logs del kernel
adb shell dmesg

# Logs de radio
adb logcat -b radio
```

### Logs Avanzados

```bash
# Dumps del sistema
adb shell dumpsys > system_dump.txt

# Dump de servicios específicos
adb shell dumpsys activity
adb shell dumpsys window
adb shell dumpsys package
adb shell dumpsys cpuinfo
adb shell dumpsys meminfo

# Información de procesos
adb shell top -n 1
adb shell ps -A

# Archivos de sistema
adb shell cat /proc/version
adb shell cat /proc/cpuinfo
adb shell cat /proc/meminfo
```

## 5. Análisis de APKs Extraídos

### Extraer y Analizar SmartTutor

```bash
# Paso 1: Extraer APK
adb pull /system/system/hidden/SmartTutor/SmartTutor.apk

# Paso 2: Analizar con apktool
apktool d SmartTutor.apk -o SmartTutor_src

# Paso 3: Ver AndroidManifest
cat SmartTutor_src/AndroidManifest.xml

# Paso 4: Buscar activities
grep -A 10 "<activity" SmartTutor_src/AndroidManifest.xml

# Paso 5: Buscar permisos
grep "<uses-permission" SmartTutor_src/AndroidManifest.xml

# Paso 6: Decompile a Java con jadx
jadx SmartTutor.apk -d SmartTutor_java

# Paso 7: Buscar strings interesantes
grep -r "password\|secret\|key\|token" SmartTutor_java/
```

### Analizar Apps de Test

```bash
# Extraer todas las apps de test
mkdir test_apps
adb pull /system/system/app/UwbTest/UwbTest.apk test_apps/
adb pull /system/system/app/WlanTest/WlanTest.apk test_apps/
adb pull /system/system/priv-app/SecFactoryPhoneTest/ test_apps/

# Análisis batch
for apk in test_apps/*.apk; do
    echo "Analyzing $apk..."
    apktool d "$apk" -o "${apk%.apk}_src"
    jadx "$apk" -d "${apk%.apk}_java"
done
```

## 6. Uso de Herramientas de Diagnóstico Qualcomm

### Preparación (requiere root)

```bash
# Habilitar puerto DIAG
adb shell
su
setprop sys.usb.config diag,adb

# Verificar configuración
getprop sys.usb.config

# Verificar dispositivo DIAG
ls -l /dev/diag*
```

### Captura con QXDM (Windows)

1. Instalar QXDM Professional
2. Configurar puerto COM (Device Manager)
3. Abrir QXDM
4. View → New Item View
5. Seleccionar logs deseados
6. Start logging

### Captura con herramientas open source

```bash
# Instalar pydiag
pip install pycrate

# Script de captura básico (Python)
cat > diag_capture.py << 'EOF'
#!/usr/bin/env python3
import serial
import sys

# Abrir puerto serial (ajustar según sistema)
port = '/dev/ttyUSB0'  # Linux
# port = 'COM3'  # Windows

try:
    ser = serial.Serial(port, 115200, timeout=1)
    print(f"Conectado a {port}")
    
    while True:
        data = ser.read(1024)
        if data:
            print(data.hex())
            
except KeyboardInterrupt:
    print("\nDetenido por usuario")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'ser' in locals():
        ser.close()
EOF

chmod +x diag_capture.py
python3 diag_capture.py
```

## 7. Análisis de Knox

### Verificar Estado de Knox

```bash
# Estado básico
adb shell getprop ro.security.knoxmatrix

# Warranty bit (Knox e-fuse)
adb shell getprop ro.boot.warranty_bit
# 0 = No activado (warranty OK)
# 1 = Activado (warranty void)

# Verified boot state
adb shell getprop ro.boot.verifiedbootstate
# green = Verificado
# orange = Bootloader desbloqueado
```

### Explorar APIs de Knox

```bash
# Listar permisos Knox
adb shell pm list permissions | grep knox

# Apps con permisos Knox
adb shell dumpsys package | grep -A 5 "com.samsung.android.knox"

# Servicios Knox activos
adb shell service list | grep knox
```

## 8. Análisis de Cámara IA

### Extraer Librerías de Cámara

```bash
# Crear directorio
mkdir camera_libs

# Extraer librerías IA
adb pull /vendor/lib/libBeauty_v4.camera.samsung.so camera_libs/
adb pull /vendor/lib/libAIMFISP.camera.samsung.so camera_libs/
adb pull /vendor/lib/libLightObjectDetector_v1.camera.samsung.so camera_libs/
adb pull /vendor/lib/libOpenCv.camera.samsung.so camera_libs/
adb pull /vendor/lib/libHprFace_GAE_api.camera.samsung.so camera_libs/

# Analizar con strings
strings camera_libs/libAIMFISP.camera.samsung.so | grep -i "model\|neural\|ai"

# Analizar con Ghidra/IDA
# 1. Cargar .so en Ghidra
# 2. Auto-análisis
# 3. Buscar funciones con nombres interesantes
# 4. Analizar flujo de datos
```

### Capturar Logs de Cámara

```bash
# Logs en tiempo real
adb logcat -s Camera:* -s CameraService:* -s mm-camera:*

# Con más detalle
adb shell setprop persist.vendor.camera.debug 1
adb shell setprop persist.vendor.camera.logMask 0xFF

# Capturar
adb logcat -b all | grep -i camera > camera_logs.txt
```

## 9. Análisis Forense

### Extraer Dumps del Kernel

```bash
# Si hay crashes recientes (requiere root)
adb shell su -c "ls -la /data/vendor/ramdump/"
adb shell su -c "ls -la /data/vendor/tombstones/"
adb shell su -c "ls -la /data/vendor/ssrdump/"

# Extraer dumps
adb pull /data/vendor/ramdump/ ./dumps/
adb pull /data/vendor/tombstones/ ./dumps/

# Persistent storage (pstore)
adb shell su -c "ls -la /sys/fs/pstore/"
adb pull /sys/fs/pstore/ ./pstore/
```

### Análisis de Dumps

```bash
# Ver tombstones (crash reports)
cd dumps/tombstones
for file in tombstone_*; do
    echo "=== $file ==="
    cat "$file" | head -50
done

# Buscar patrones de crash
grep -r "SIGSEGV\|SIGABRT\|SIGILL" dumps/

# Analizar stack traces
grep -A 20 "backtrace:" dumps/tombstones/*
```

## 10. Monitoreo de Telemetría

### DiagMonAgent

```bash
# Monitorear actividad de DiagMonAgent
adb logcat -s DiagMonAgent:*

# Ver conexiones de red
adb shell netstat -an | grep -i established

# Capturar tráfico (requiere root + tcpdump)
adb shell su -c "tcpdump -i any -s 0 -w /sdcard/capture.pcap"
# Dejar capturar, luego Ctrl+C
adb pull /sdcard/capture.pcap
# Analizar con Wireshark
```

## 11. Búsqueda de Códigos Secretos Adicionales

### Script Automatizado

```bash
#!/bin/bash
# find_secret_codes.sh

echo "Buscando códigos secretos en APKs..."

# Directorio temporal
WORK_DIR="secret_codes_work"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# Lista de APKs a analizar
APKS=(
    "/system/system/priv-app/SecFactoryPhoneTest/SecFactoryPhoneTest.apk"
    "/system/system/priv-app/DiagMonAgent95/DiagMonAgent95.apk"
    "/system/system/app/UwbTest/UwbTest.apk"
    "/system/system/app/WlanTest/WlanTest.apk"
)

# Extraer y analizar
for apk_path in "${APKS[@]}"; do
    apk_name=$(basename "$apk_path")
    echo "Analizando $apk_name..."
    
    # Extraer
    adb pull "$apk_path" 2>/dev/null
    
    if [ -f "$apk_name" ]; then
        # Decompile
        apktool d "$apk_name" -o "${apk_name%.apk}_src" -f
        
        # Buscar códigos
        echo "=== Códigos encontrados en $apk_name ==="
        grep -rh "android_secret_code://" "${apk_name%.apk}_src/" | \
            sed 's/.*android_secret_code:\/\///g' | \
            sed 's/["\/>].*//g' | \
            sort -u
        
        # Buscar en strings.xml
        find "${apk_name%.apk}_src/" -name "strings.xml" -exec \
            grep -H "secret\|code\|hidden" {} \;
    fi
done

echo "Análisis completo. Revisa los resultados arriba."
```

## 12. Exportar Información Completa del Dispositivo

### Script Completo de Exportación

```bash
#!/bin/bash
# export_device_info.sh

OUTPUT_DIR="device_export_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

echo "Exportando información del dispositivo a $OUTPUT_DIR..."

# Información básica
echo "=== Device Info ===" > "$OUTPUT_DIR/device_info.txt"
adb shell getprop >> "$OUTPUT_DIR/device_info.txt"

# Packages
echo "Exportando lista de packages..."
adb shell pm list packages -f > "$OUTPUT_DIR/packages.txt"

# Logs
echo "Exportando logs..."
adb logcat -d > "$OUTPUT_DIR/logcat.txt"
adb shell dmesg > "$OUTPUT_DIR/dmesg.txt"

# Sistema
echo "Exportando información del sistema..."
adb shell dumpsys > "$OUTPUT_DIR/dumpsys_full.txt"
adb shell ps -A > "$OUTPUT_DIR/processes.txt"
adb shell top -n 1 > "$OUTPUT_DIR/top.txt"
adb shell df -h > "$OUTPUT_DIR/disk_usage.txt"
adb shell mount > "$OUTPUT_DIR/mounts.txt"

# Batería
echo "Exportando info de batería..."
adb shell dumpsys battery > "$OUTPUT_DIR/battery.txt"

# Sensores
echo "Exportando info de sensores..."
adb shell dumpsys sensorservice > "$OUTPUT_DIR/sensors.txt"

# Red
echo "Exportando info de red..."
adb shell dumpsys connectivity > "$OUTPUT_DIR/connectivity.txt"
adb shell dumpsys wifi > "$OUTPUT_DIR/wifi.txt"

# Seguridad
echo "Exportando info de seguridad..."
echo "Knox: $(adb shell getprop ro.security.knoxmatrix)" > "$OUTPUT_DIR/security.txt"
echo "Warranty: $(adb shell getprop ro.boot.warranty_bit)" >> "$OUTPUT_DIR/security.txt"
echo "Verified Boot: $(adb shell getprop ro.boot.verifiedbootstate)" >> "$OUTPUT_DIR/security.txt"
echo "SELinux: $(adb shell getenforce)" >> "$OUTPUT_DIR/security.txt"

echo "Exportación completa en: $OUTPUT_DIR"
echo "Comprimiendo..."
tar -czf "${OUTPUT_DIR}.tar.gz" "$OUTPUT_DIR"
echo "Archivo generado: ${OUTPUT_DIR}.tar.gz"
```

## 13. Pruebas de Seguridad (Ethical Hacking)

### Verificar Superficie de Ataque

```bash
# Listar puertos abiertos
adb shell netstat -tuln

# Servicios expuestos
adb shell service list | wc -l

# Apps con permisos peligrosos
adb shell pm list permissions -g -d

# Verificar componentes exportados
for pkg in $(adb shell pm list packages | cut -d: -f2); do
    echo "Package: $pkg"
    adb shell dumpsys package "$pkg" | \
        grep -A 3 "exported=true"
done
```

### Test de Permisos Excesivos

```bash
# Apps con permisos SYSTEM
adb shell pm list packages -s

# Apps con uid system
adb shell ps -A | grep " system "

# Apps que pueden ejecutar como root
adb shell find /system -perm -4000 -ls
```

## ⚠️ Consideraciones Importantes

### Antes de Ejecutar Comandos

1. **Backup**: Siempre haz backup completo
2. **Test Device**: Usa dispositivo de test si es posible
3. **Knox**: Algunos comandos activarán Knox e-fuse
4. **Root**: Muchos comandos requieren root
5. **USB Debugging**: Debe estar habilitado

### Legalidad y Ética

- ✅ Usa en TU dispositivo
- ✅ Para aprendizaje e investigación
- ✅ Respeta términos de servicio
- ❌ No uses en dispositivos de terceros sin permiso
- ❌ No distribuyas software propietario
- ❌ No uses para actividades ilegales

### Reversibilidad

Algunos cambios son **IRREVERSIBLES**:
- Knox e-fuse (warranty bit)
- Bootloader unlock
- Modificaciones a particiones del sistema

---

**Documento**: Ejemplos prácticos de uso
**Fecha**: 2025-12-28
**Advertencia**: Úsalo bajo tu propio riesgo
**Propósito**: Educación e investigación
