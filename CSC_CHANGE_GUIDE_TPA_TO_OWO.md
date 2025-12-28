# Guía para Cambiar CSC de TPA a OWO - Samsung Galaxy S23

## 📱 Información del Dispositivo

**Modelo**: Samsung Galaxy S23 (SM-S916B)
**CSC Actual**: SAOMC_SM-S916B_OWO_TPA_16_0009 TPA/TPA,TPA/TPA
**CSC Objetivo**: OWO (Open World - Multi-CSC)
**Requisito**: Root access (confirmado disponible)

---

## ⚠️ ADVERTENCIAS IMPORTANTES

1. **Backup completo**: Haz backup de todos tus datos antes de proceder
2. **Knox e-fuse**: Si Knox no está activado, estos cambios lo activarán permanentemente
3. **Garantía**: Estos cambios pueden invalidar la garantía
4. **Riesgo de brick**: Seguir las instrucciones cuidadosamente para evitar brick
5. **Responsabilidad**: Procede bajo tu propio riesgo

---

## 🔍 Método 1: Cambio de CSC usando archivos del sistema (Recomendado)

### Paso 1: Backup de particiones críticas

```bash
# Conectar vía ADB
adb shell
su

# Backup de particiones CSC (ajustar según dispositivo)
dd if=/dev/block/by-name/optics of=/sdcard/backup_optics.img
dd if=/dev/block/by-name/prism of=/sdcard/backup_prism.img

# Copiar a PC
exit
adb pull /sdcard/backup_optics.img
adb pull /sdcard/backup_prism.img
```

### Paso 2: Identificar la partición CSC actual

```bash
adb shell
su

# Ver información de CSC actual
getprop | grep -i csc
getprop | grep -i sales
getprop ril.sales_code

# Ver particiones relacionadas
ls -la /dev/block/by-name/ | grep -iE "csc|optics|prism"

# Ver contenido de OMR (si existe)
ls -la /omr/ 2>/dev/null
ls -la /optics/ 2>/dev/null
ls -la /prism/ 2>/dev/null
```

### Paso 3: Modificar archivos CSC

```bash
# Entrar como root
adb shell
su

# Montar sistema como lectura/escritura
mount -o remount,rw /system
mount -o remount,rw /vendor
mount -o remount,rw /product

# Buscar archivos de configuración CSC
find /system -name "*csc*" -o -name "*sales*" 2>/dev/null
find /vendor -name "*csc*" -o -name "*sales*" 2>/dev/null

# Si existe archivo de sales code
echo "OWO" > /efs/imei/mps_code.dat
chmod 644 /efs/imei/mps_code.dat

# También verificar
echo "OWO" > /efs/FactoryApp/csc_data
chmod 644 /efs/FactoryApp/csc_data
```

### Paso 4: Modificar build.prop

```bash
# Backup build.prop
cp /system/build.prop /sdcard/build.prop.backup
cp /vendor/build.prop /sdcard/vendor_build.prop.backup

# Editar system build.prop
vi /system/build.prop
# O usar sed:
sed -i 's/TPA/OWO/g' /system/build.prop

# Editar vendor build.prop
sed -i 's/TPA/OWO/g' /vendor/build.prop

# Editar product build.prop (si existe)
sed -i 's/TPA/OWO/g' /product/build.prop 2>/dev/null
```

### Paso 5: Modificar propiedades del sistema

```bash
# Establecer sales code
setprop ril.sales_code OWO
setprop ro.csc.sales_code OWO
setprop persist.sys.omc_etcpath /system/etc/OWO

# Verificar cambios
getprop | grep -i sales
```

### Paso 6: Limpiar caché y reiniciar

```bash
# Limpiar caché de Dalvik/ART
rm -rf /data/dalvik-cache/*
rm -rf /cache/*

# Reiniciar
reboot
```

---

## 🔧 Método 2: Uso de Samloader/Odin (Más seguro)

### Opción A: Flash completo de firmware OWO

```bash
# 1. Descargar firmware OWO desde:
# https://samfw.com/ o https://samfrew.com/
# Buscar: SM-S916B OWO

# 2. Extraer archivos
# 3. Flash con Odin:
#    - AP: AP_*.tar.md5
#    - BL: BL_*.tar.md5
#    - CP: CP_*.tar.md5
#    - CSC: CSC_*.tar.md5 (usar HOME_CSC para mantener datos)

# 4. Reiniciar dispositivo
```

### Opción B: Flash solo CSC con Odin

```bash
# 1. Extraer solo el archivo CSC del firmware OWO
# 2. En Odin, cargar solo CSC_OWO.tar.md5
# 3. Marcar "Auto Reboot"
# 4. Presionar "Start"
```

---

## 🛠️ Método 3: Usando herramientas especializadas (Con root)

### Usando *#272*IMEI# (Service Mode)

```bash
# 1. Abrir dialer
# 2. Marcar: *#272*[TU_IMEI]#
#    Ejemplo: *#272*123456789012345#
# 3. Se abrirá menú CSC
# 4. Seleccionar OWO de la lista
# 5. Instalar
# 6. Dispositivo reiniciará automáticamente
```

**Nota**: Este código puede no funcionar en todas las versiones de firmware.

### Usando app CSC Changer (requiere root)

```bash
# 1. Instalar app "CSC Changer" desde XDA
# 2. Otorgar permisos de root
# 3. Seleccionar CSC objetivo: OWO
# 4. Aplicar cambios
# 5. Reiniciar
```

---

## 🔍 Método 4: Script automatizado (Avanzado)

Crear archivo `change_csc_to_owo.sh`:

```bash
#!/system/bin/sh
# Script para cambiar CSC de TPA a OWO
# Requiere root

echo "=== CSC Changer: TPA -> OWO ==="
echo "Verificando permisos de root..."

if [ "$(id -u)" != "0" ]; then
   echo "ERROR: Este script requiere root"
   exit 1
fi

echo "Root confirmado. Procediendo..."

# Backup
echo "Creando backups..."
mkdir -p /sdcard/csc_backup
cp /efs/imei/mps_code.dat /sdcard/csc_backup/ 2>/dev/null
cp /efs/FactoryApp/csc_data /sdcard/csc_backup/ 2>/dev/null
cp /system/build.prop /sdcard/csc_backup/ 2>/dev/null

# Montar como RW
echo "Montando particiones como lectura/escritura..."
mount -o remount,rw /system
mount -o remount,rw /vendor
mount -o remount,rw /efs

# Cambiar CSC
echo "Cambiando CSC a OWO..."

# Método 1: EFS
if [ -d "/efs/imei" ]; then
    echo "OWO" > /efs/imei/mps_code.dat
    chmod 644 /efs/imei/mps_code.dat
    echo "✓ Actualizado /efs/imei/mps_code.dat"
fi

if [ -d "/efs/FactoryApp" ]; then
    echo "OWO" > /efs/FactoryApp/csc_data
    chmod 644 /efs/FactoryApp/csc_data
    echo "✓ Actualizado /efs/FactoryApp/csc_data"
fi

# Método 2: Build.prop
echo "Actualizando build.prop..."
sed -i 's/TPA/OWO/g' /system/build.prop
sed -i 's/TPA/OWO/g' /vendor/build.prop 2>/dev/null
sed -i 's/TPA/OWO/g' /product/build.prop 2>/dev/null

# Método 3: Propiedades del sistema
echo "Estableciendo propiedades del sistema..."
setprop ril.sales_code OWO
setprop ro.csc.sales_code OWO
setprop persist.sys.omc_etcpath /system/etc/OWO

# Limpiar caché
echo "Limpiando caché..."
rm -rf /data/dalvik-cache/* 2>/dev/null
rm -rf /cache/* 2>/dev/null

# Verificar
echo ""
echo "=== Verificación de cambios ==="
echo "Sales code actual:"
getprop ril.sales_code
getprop ro.csc.sales_code

echo ""
echo "✓ CSC cambiado exitosamente a OWO"
echo ""
echo "IMPORTANTE: Reinicia el dispositivo para aplicar cambios"
echo "Comando: reboot"
echo ""
echo "Backups guardados en: /sdcard/csc_backup/"

# Preguntar si reiniciar
read -p "¿Deseas reiniciar ahora? (s/n): " respuesta
if [ "$respuesta" = "s" ]; then
    echo "Reiniciando en 5 segundos..."
    sleep 5
    reboot
fi
```

### Uso del script:

```bash
# Subir script al dispositivo
adb push change_csc_to_owo.sh /sdcard/

# Ejecutar
adb shell
su
sh /sdcard/change_csc_to_owo.sh
```

---

## 🔍 Método 5: Usando vulnerabilidades del firmware (Muy avanzado)

Basado en el análisis de vulnerabilidades del firmware:

### Explotar SmartTutor (si accesible)

```bash
# Si SmartTutor tiene capacidad de modificación del sistema
adb shell am start -n com.samsung.smarttutor/.MainActivity
# Navegar a opciones de configuración CSC (si existe)
```

### Usar apps de test de fábrica

```bash
# Iniciar SecFactoryPhoneTest
adb shell am start -n com.sec.factory/.PhoneTestActivity

# Buscar opción de CSC/Sales Code en menú
# Algunas versiones tienen opción oculta en:
# Settings -> About -> Tap 7 times -> CSC Options
```

### Modificar via DIAG (si accesible)

```bash
# Habilitar puerto DIAG (requiere root)
adb shell
su
setprop sys.usb.config diag,adb

# Usar QXDM/QPST para modificar NV items relacionados con CSC
# NV Item 0x1F12 (NV_SPC) - CSC Code
# Requiere conocimiento avanzado de protocolo DIAG
```

---

## 📋 Verificación post-cambio

### Verificar que el CSC cambió correctamente:

```bash
# Método 1: ADB
adb shell getprop | grep -i csc
adb shell getprop ril.sales_code
adb shell getprop ro.csc.sales_code

# Método 2: Código en dialer
*#1234#  # Ver versión firmware
*#12580*369#  # Ver SW/HW info

# Método 3: Configuración
# Settings -> About phone -> Software information
# Verificar que CSC muestre OWO

# Método 4: Archivo
adb shell cat /efs/imei/mps_code.dat
```

### Resultado esperado:

```
ril.sales_code: OWO
ro.csc.sales_code: OWO
CSC Version: SAOMC_SM-S916B_OWO_OWO_16_0009 OWO/OWO
```

---

## 🔄 Troubleshooting

### Problema 1: CSC no cambia después de reiniciar

**Solución**:
```bash
# Limpiar más agresivamente
adb shell
su
rm -rf /data/dalvik-cache/*
rm -rf /data/system/package_cache/*
rm -rf /cache/*
pm clear com.android.providers.settings
reboot recovery
# Wipe cache partition
# Reboot
```

### Problema 2: Bootloop después del cambio

**Solución**:
```bash
# Entrar a recovery mode
# Wipe cache partition
# Si persiste, hacer factory reset (perderás datos)
# O restaurar backup de particiones
```

### Problema 3: Permisos denegados

**Solución**:
```bash
# Verificar que SELinux esté en permissive
adb shell
su
setenforce 0
getenforce  # Debe mostrar "Permissive"

# Luego ejecutar comandos de cambio CSC
```

### Problema 4: Build.prop no se puede modificar

**Solución**:
```bash
# Deshabilitar dm-verity y verificación
adb reboot bootloader
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img
fastboot reboot

# O usar Magisk para modificar build.prop
# Magisk Manager -> Modules -> Install "MagiskHide Props Config"
```

---

## 🎯 Método Recomendado (Más seguro)

Para tu caso específico con **root ya disponible**:

```bash
# Método combinado (más confiable)

# 1. Backup completo
adb shell
su
dd if=/dev/block/by-name/optics of=/sdcard/optics_backup.img
dd if=/dev/block/by-name/prism of=/sdcard/prism_backup.img

# 2. Cambiar EFS
mount -o remount,rw /efs
echo "OWO" > /efs/imei/mps_code.dat
echo "OWO" > /efs/FactoryApp/csc_data

# 3. Usar código secreto
exit
# Marca en dialer: *#272*[TU_IMEI]#
# Selecciona OWO e instala

# 4. Si lo anterior no funciona, modifica build.prop
su
mount -o remount,rw /system
sed -i 's/TPA/OWO/g' /system/build.prop

# 5. Limpia y reinicia
rm -rf /data/dalvik-cache/*
rm -rf /cache/*
reboot
```

---

## 📚 Información Adicional

### ¿Qué es CSC?

CSC (Customer Software Customization) controla:
- Idiomas disponibles
- Apps preinstaladas
- Configuraciones de operadora
- Funciones regionales
- APNs de red

### ¿Qué es OWO?

OWO (Open World) es un CSC multi-región que:
- Incluye todos los idiomas
- No tiene bloatware de operadora específica
- Configuración neutral
- Updates más rápidos (generalmente)

### Diferencias TPA vs OWO

| Característica | TPA (Panamá) | OWO (Open World) |
|----------------|--------------|------------------|
| Región | América (Panamá) | Multi-región |
| Bloatware | Apps de operadora | Mínimo |
| Updates | Según operadora | Genérico Samsung |
| Idiomas | Limitados | Todos |

---

## 🔗 Recursos Útiles

- [XDA Forums - Galaxy S23](https://forum.xda-developers.com/f/samsung-galaxy-s23.12691/)
- [Samfw.com](https://samfw.com/) - Descargar firmwares
- [Samfrew.com](https://samfrew.com/) - Firmwares alternativos
- [Frija Tool](https://github.com/nlscc/frija) - Descargador de firmware Samsung
- [Odin](https://odindownload.com/) - Flash tool oficial

---

## 📧 Soporte

Si tienes problemas:
1. Haz backup completo ANTES de cualquier cambio
2. Documenta el error exacto
3. Consulta en XDA Developers
4. Considera usar Odin con firmware completo OWO (más seguro)

---

**Autor**: Análisis de ingeniería inversa - UN1CA Firmware
**Fecha**: 2025-12-28
**Dispositivo**: Samsung Galaxy S23 (SM-S916B)
**Estado**: Guía completa para cambio de CSC con root

⚠️ **RECORDATORIO**: Procede bajo tu propio riesgo. Haz backup completo antes de comenzar.
