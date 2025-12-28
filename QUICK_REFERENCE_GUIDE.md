# Guía Rápida - Comandos y Códigos Útiles

## 📱 Códigos Secretos del Dialer

Ingresa estos códigos en el marcador telefónico:

| Código | Función | Descripción |
|--------|---------|-------------|
| `*#0*#` | Hardware Test | Menú completo de tests de hardware |
| `*#0228#` | Battery Status | Estado detallado de batería |
| `*#12580*369#` | SW/HW Info | Información de software y hardware |
| `*#9900#` | SysDump | Modo de volcado del sistema |
| `*#0808#` | USB Settings | Configuración de conexión USB |
| `*#2663#` | TSP/TSC Info | Información del touchscreen |
| `*#0011#` | Service Mode | Información de red y señal |
| `*#232337#` | Bluetooth MAC | Dirección MAC Bluetooth |
| `*#232338#` | WiFi MAC | Dirección MAC WiFi |
| `*#1234#` | Firmware Version | Versión del firmware detallada |

## 🔧 Comandos ADB Útiles

### Información del Sistema

```bash
# Verificar conexión
adb devices

# Información del dispositivo
adb shell getprop ro.product.model
adb shell getprop ro.build.PDA
adb shell getprop ro.build.version.release

# Estado de Knox
adb shell getprop ro.security.knoxmatrix

# Estado de SELinux
adb shell getenforce

# Verificar root
adb shell su -c "id"
```

### Activar Funciones Ocultas

```bash
# Iniciar SmartTutor oculto
adb shell am start -n com.samsung.smarttutor/.MainActivity

# Iniciar tests de fábrica
adb shell am start -n com.sec.factory/.PhoneTestActivity

# Iniciar test de WiFi
adb shell am start -n com.sec.android.app.wlantest/.WlanTest

# Iniciar test UWB
adb shell am start -n com.sec.android.app.uwbtest/.UWBTest

# Información del dispositivo detallada
adb shell dumpsys battery
adb shell dumpsys display
adb shell dumpsys sensors
```

### Logs y Diagnóstico

```bash
# Ver logs en tiempo real
adb logcat

# Logs filtrados
adb logcat -s Knox
adb logcat -s DiagMonAgent
adb logcat -s SecurityLog

# Guardar logs
adb logcat -d > logcat.txt

# Información de procesos
adb shell ps -A | grep -i diag
adb shell ps -A | grep -i knox

# Ver servicios activos
adb shell service list | grep -i diag
```

### Extraer APKs

```bash
# Listar packages instalados
adb shell pm list packages -f | grep -i test
adb shell pm list packages -f | grep -i factory
adb shell pm list packages -f | grep -i knox

# Extraer APK específico
adb shell pm path com.sec.factory
adb pull /system/app/[path]/app.apk

# Extraer SmartTutor oculto
adb pull /system/system/hidden/SmartTutor/SmartTutor.apk ./SmartTutor.apk

# Extraer todos los tests
adb pull /system/system/app/UwbTest/UwbTest.apk
adb pull /system/system/app/WlanTest/WlanTest.apk
adb pull /system/system/priv-app/SecFactoryPhoneTest/SecFactoryPhoneTest.apk
```

### Configuración USB y Diagnóstico (requiere root)

```bash
# Habilitar modo diagnóstico
adb shell su -c "setprop sys.usb.config diag,adb"

# Ver configuración USB actual
adb shell getprop sys.usb.config

# Habilitar logging verbose
adb shell su -c "setprop persist.vendor.verbose_logging 1"
```

## 📊 Comandos de Sistema (shell interactivo)

```bash
# Entrar a shell
adb shell

# Ver propiedades del sistema
getprop | grep -i knox
getprop | grep -i debug
getprop | grep -i security

# Información de particiones
df -h
mount | grep -i system

# Ver módulos del kernel cargados
lsmod
cat /proc/modules

# Información de CPU
cat /proc/cpuinfo

# Información de memoria
cat /proc/meminfo
free -h

# Ver sensores
cat /sys/class/sensors/*/name

# Información de batería
cat /sys/class/power_supply/battery/capacity
cat /sys/class/power_supply/battery/status
cat /sys/class/power_supply/battery/health

# Temperatura
cat /sys/class/thermal/thermal_zone*/temp
```

## 🔍 Análisis de APKs

### Con apktool

```bash
# Instalar apktool
# Download from https://ibotpeaches.github.io/Apktool/

# Decompile APK
apktool d SmartTutor.apk -o SmartTutor_decompiled

# Ver manifest
cat SmartTutor_decompiled/AndroidManifest.xml

# Buscar códigos secretos
grep -r "SECRET_CODE" SmartTutor_decompiled/
grep -r "android_secret_code" SmartTutor_decompiled/

# Buscar activities
grep -r "activity" SmartTutor_decompiled/AndroidManifest.xml
```

### Con jadx (decompile a Java)

```bash
# Instalar jadx
# Download from https://github.com/skylot/jadx

# Decompile
jadx SmartTutor.apk -d SmartTutor_java

# Analizar código
cd SmartTutor_java
grep -r "password" .
grep -r "secret" .
grep -r "hidden" .
```

## 🛠️ Herramientas Recomendadas

### Para Análisis de Firmware

- **[Android Kitchen](https://forum.xda-developers.com/t/tool-android-image-kitchen.2073775/)** - Unpack/repack boot.img
- **[payload-dumper-go](https://github.com/ssut/payload-dumper-go)** - Extraer OTA payloads
- **[simg2img](https://github.com/anestisb/android-simg2img)** - Convertir sparse images
- **[bindiff](https://github.com/google/bindiff)** - Comparar binarios

### Para Análisis de APKs

- **[apktool](https://ibotpeaches.github.io/Apktool/)** - Decompile/recompile APKs
- **[jadx](https://github.com/skylot/jadx)** - Decompile a Java
- **[Mobile Security Framework (MobSF)](https://github.com/MobSF/Mobile-Security-Framework-MobSF)** - Análisis de seguridad
- **[androguard](https://github.com/androguard/androguard)** - Análisis estático y dinámico

### Para Análisis de Binarios

- **[Ghidra](https://ghidra-sre.org/)** - NSA reverse engineering tool
- **[IDA Pro](https://hex-rays.com/ida-pro/)** - Industry standard (comercial)
- **[Binary Ninja](https://binary.ninja/)** - Reverse engineering platform
- **[radare2](https://rada.re/)** - Open source framework

### Para Runtime Analysis

- **[Frida](https://frida.re/)** - Dynamic instrumentation toolkit
- **[Xposed Framework](https://repo.xposed.info/)** - Hook framework (requiere root)
- **[Magisk](https://github.com/topjohnwu/Magisk)** - Root manager moderno
- **[LSPosed](https://github.com/LSPosed/LSPosed)** - Xposed para Magisk

### Para Diagnóstico Qualcomm

- **QXDM Professional** - Qualcomm diagnostic monitor (oficial)
- **QPST** - Qualcomm Product Support Tools
- **[pydiag](https://github.com/P1sec/pycrate)** - Python DIAG implementation
- **[scat](https://github.com/fgsect/scat)** - Samsung Cellular Analysis Tool

## 🔬 Scripts Útiles

### Script para Extraer Toda la Info

```bash
#!/bin/bash
# extract_device_info.sh

echo "=== Device Information ==="
adb shell getprop ro.product.model
adb shell getprop ro.build.PDA
adb shell getprop ro.build.version.release

echo -e "\n=== Knox Status ==="
adb shell getprop ro.security.knoxmatrix

echo -e "\n=== Apps Installed ==="
adb shell pm list packages -f > packages.txt
cat packages.txt | wc -l
echo "Total packages saved to packages.txt"

echo -e "\n=== Extracting Logs ==="
adb logcat -d > logcat_full.txt
echo "Logcat saved to logcat_full.txt"

echo -e "\n=== System Properties ==="
adb shell getprop > props.txt
echo "Properties saved to props.txt"

echo -e "\n=== Running Processes ==="
adb shell ps -A > processes.txt
echo "Processes saved to processes.txt"

echo -e "\n=== Services ==="
adb shell service list > services.txt
echo "Services saved to services.txt"

echo "Done! Check generated files for details."
```

### Script para Buscar Códigos Secretos

```bash
#!/bin/bash
# find_secret_codes.sh

echo "Pulling APKs for analysis..."

# Crear directorio de trabajo
mkdir -p secret_codes_analysis
cd secret_codes_analysis

# Extraer APKs de test
adb pull /system/system/priv-app/SecFactoryPhoneTest/SecFactoryPhoneTest.apk 2>/dev/null
adb pull /system/system/priv-app/DiagMonAgent95/DiagMonAgent95.apk 2>/dev/null
adb pull /system/system/app/UwbTest/UwbTest.apk 2>/dev/null
adb pull /system/system/app/WlanTest/WlanTest.apk 2>/dev/null

echo "Decompiling APKs..."

for apk in *.apk; do
    if [ -f "$apk" ]; then
        echo "Processing $apk..."
        apktool d "$apk" -o "${apk%.apk}_decompiled" -f
        
        # Buscar códigos secretos
        echo "Searching for secret codes in $apk..."
        grep -r "android_secret_code" "${apk%.apk}_decompiled/" 2>/dev/null
        grep -r "SECRET_CODE" "${apk%.apk}_decompiled/" 2>/dev/null
    fi
done

echo "Analysis complete! Check the decompiled folders for details."
```

## 📖 Referencias Rápidas

### Estructura de Particiones

```
/system         - Sistema Android base
/vendor         - Componentes del fabricante
/product        - Apps de producto
/odm            - Customización OEM
/system_ext     - Extensiones del sistema
/data           - Datos de usuario
/cache          - Caché temporal
/metadata       - Metadata del sistema
```

### Ubicaciones Importantes

```
# Apps ocultas
/system/system/hidden/

# Apps de test
/system/system/app/*Test/
/system/system/priv-app/*Test*/

# Binarios de diagnóstico
/vendor/bin/diag*
/vendor/bin/test_*

# Módulos del kernel
/vendor_dlkm/lib/modules/
/system_dlkm/lib/modules/

# Logs
/data/log/
/data/vendor/log/
/sys/fs/pstore/

# Init scripts
/system/etc/init/
/vendor/etc/init/

# Propiedades
*.prop files
```

### Permisos Importantes

```xml
<!-- Lectura de logs del sistema -->
android.permission.READ_LOGS

<!-- Diagnóstico -->
android.permission.DUMP

<!-- Reboot -->
android.permission.REBOOT

<!-- Shell commands -->
android.permission.EXECUTE_SHELL_COMMAND

<!-- Knox -->
com.samsung.android.knox.permission.*
```

## ⚠️ Advertencias

1. **No uses estos comandos si no sabes lo que hacen**
2. **Modificar el sistema puede causar brick**
3. **Activar funciones ocultas puede invalidar la garantía**
4. **El uso de herramientas de diagnóstico puede violar términos de servicio**
5. **Siempre haz backup antes de modificar el sistema**
6. **Knox e-fuse es PERMANENTE cuando se activa**
7. **Algunos comandos requieren root (SU)**

## 📱 Estado de Knox

```bash
# Verificar Knox
adb shell getprop ro.boot.warranty_bit
# 0 = No activado (bueno)
# 1 = Activado (permanente)

# Verificar bootloader
adb shell getprop ro.boot.verifiedbootstate
# green = Verificado
# orange = Desbloqueado
# red = Error de verificación
```

## 🔐 Desbloquear Bootloader (PRECAUCIÓN)

**Samsung Galaxy S23 - OEM Unlock**

1. Habilitar opciones de desarrollador (tap 7 veces en número de compilación)
2. Entrar a Opciones de desarrollador
3. Habilitar "OEM unlocking"
4. Apagar el dispositivo
5. Boot en modo download (Vol Up + Vol Down + USB conectado)
6. Vol Up para confirmar unlock (ESTO ACTIVA KNOX E-FUSE)
7. El dispositivo hará factory reset

**ADVERTENCIA**: Esto es IRREVERSIBLE y:
- Activa Knox e-fuse permanentemente
- Invalida la garantía
- Samsung Pay no funcionará nunca más
- Secure Folder dejará de funcionar
- Algunas apps bancarias no funcionarán

---

**Guía Rápida**: Comandos útiles para análisis
**Fecha**: 2025-12-28
**Dispositivo**: Samsung Galaxy S23 (SM-S916B)
**Firmware**: S916BXXS8EYK5
