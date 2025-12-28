# Lista Completa de Servicios, Archivos y Comandos para Modificación CSC

## 🎯 Resumen Ejecutivo

Este documento proporciona una lista exhaustiva de TODOS los servicios, archivos, propiedades y comandos shell necesarios para modificar el CSC de TPA a OWO en el Samsung Galaxy S23+ (SM-S916B).

---

## 📁 PARTE 1: ARCHIVOS CRÍTICOS A MODIFICAR

### 1.1. Partición EFS (CRÍTICO - Prioridad Máxima)

```
Ubicación: /efs/imei/
```

| Archivo | Función | Modificación Requerida |
|---------|---------|----------------------|
| `/efs/imei/mps_code.dat` | Multi-CSC Sales Code | `echo "OWO" > /efs/imei/mps_code.dat` |
| `/efs/imei/sales_code.dat` | Sales Code principal | `echo "OWO" > /efs/imei/sales_code.dat` |
| `/efs/imei/replace_code.dat` | Código de reemplazo | `echo "OWO" > /efs/imei/replace_code.dat` |
| `/efs/imei/selective` | Configuración selectiva | Verificar existencia |

**Comando Completo EFS:**
```bash
#!/system/bin/sh
# Modificación completa de EFS

mount -o remount,rw /efs

# Backup
cp /efs/imei/mps_code.dat /sdcard/mps_code.dat.bak
cp /efs/imei/sales_code.dat /sdcard/sales_code.dat.bak
cp /efs/imei/replace_code.dat /sdcard/replace_code.dat.bak 2>/dev/null

# Modificar
echo "OWO" > /efs/imei/mps_code.dat
echo "OWO" > /efs/imei/sales_code.dat
echo "OWO" > /efs/imei/replace_code.dat

# Permisos
chown radio:radio /efs/imei/mps_code.dat
chown radio:radio /efs/imei/sales_code.dat
chown radio:radio /efs/imei/replace_code.dat
chmod 0644 /efs/imei/mps_code.dat
chmod 0644 /efs/imei/sales_code.dat
chmod 0644 /efs/imei/replace_code.dat

sync
mount -o remount,ro /efs
```

### 1.2. Vendor EFS (Telephony Props)

```
Ubicación: /mnt/vendor/efs/
```

| Archivo | Función | Acción |
|---------|---------|--------|
| `/mnt/vendor/efs/telephony.prop` | Propiedades de telefonía | Modificar sales_code |
| `/mnt/vendor/efs/factory.prop` | Propiedades de fábrica | Verificar/Modificar |

**Comando:**
```bash
# Modificar telephony.prop
if [ -f /mnt/vendor/efs/telephony.prop ]; then
    sed -i 's/ro.csc.sales_code=.*/ro.csc.sales_code=OWO/' /mnt/vendor/efs/telephony.prop
    sed -i 's/ril.sales_code=.*/ril.sales_code=OWO/' /mnt/vendor/efs/telephony.prop
    # Si no existe, agregar
    grep -q "ro.csc.sales_code" /mnt/vendor/efs/telephony.prop || echo "ro.csc.sales_code=OWO" >> /mnt/vendor/efs/telephony.prop
fi
```

### 1.3. Build.prop Files

| Archivo | Modificación |
|---------|-------------|
| `/system/build.prop` | Agregar/modificar ro.csc.sales_code=OWO |
| `/vendor/build.prop` | Agregar/modificar ro.csc.sales_code=OWO |
| `/product/etc/build.prop` | Verificar y modificar si existe |
| `/odm/etc/build.prop` | Verificar y modificar si existe |

**Script Completo:**
```bash
#!/system/bin/sh
# Modificar todos los build.prop

modify_buildprop() {
    local file="$1"
    if [ -f "$file" ]; then
        echo "Modificando $file..."
        cp "$file" "${file}.bak"
        
        # Remover líneas antiguas
        sed -i '/ro.csc.sales_code=/d' "$file"
        sed -i '/persist.sys.sec_cid=/d' "$file"
        sed -i '/ril.sales_code=/d' "$file"
        
        # Agregar nuevas
        echo "" >> "$file"
        echo "# CSC Modified to OWO" >> "$file"
        echo "ro.csc.sales_code=OWO" >> "$file"
        echo "persist.sys.sec_cid=OWO" >> "$file"
        echo "ril.sales_code=OWO" >> "$file"
        
        sync
    fi
}

# Remontar particiones
mount -o remount,rw /
mount -o remount,rw /system
mount -o remount,rw /vendor
mount -o remount,rw /product
mount -o remount,rw /odm

# Modificar archivos
modify_buildprop /system/build.prop
modify_buildprop /vendor/build.prop
modify_buildprop /product/etc/build.prop
modify_buildprop /odm/etc/build.prop

# Remontar como RO
mount -o remount,ro /system
mount -o remount,ro /vendor
mount -o remount,ro /product
mount -o remount,ro /odm
mount -o remount,ro /
```

---

## 🔧 PARTE 2: PROPIEDADES DEL SISTEMA

### 2.1. Propiedades Read-Only (ro.*)

Estas propiedades se leen al boot desde build.prop y EFS:

```bash
# Verificar propiedades actuales
getprop ro.csc.sales_code
getprop ro.csc.country_code
getprop ro.csc.countryiso_code

# Nota: No se pueden modificar en runtime, requieren modificar build.prop y reiniciar
```

### 2.2. Propiedades Persist (persist.*)

Estas propiedades PERSISTEN después de reinicio y PUEDEN modificarse:

```bash
#!/system/bin/sh
# Modificar TODAS las propiedades persist relacionadas con CSC

# CSC Core
setprop persist.sys.sec_cid OWO
setprop persist.sys.sec_pcid OWO
setprop persist.sys.sec_operator OWO
setprop persist.sys.matched_code OWO
setprop persist.sys.sec_cid_ver 16_0009

# OMC (Open Market Customization)
setprop persist.sys.omc_path /system/csc/OWO
setprop persist.sys.omc_root /system/csc/OWO
setprop persist.sys.omc_support true
setprop persist.sys.omcnw_path /data/omc/OWO

# Activación
setprop persist.sys.singlesku_activate 1
setprop persist.sys.activation_result success

# RIL
setprop persist.ril.matched_code OWO
setprop persist.ril.sales_network_code OWO

# Radio
setprop persist.radio.def_network 33
setprop persist.radio.multisim.config dsds

# Verificar cambios
getprop | grep persist.sys | grep -E "cid|omc|matched"
getprop | grep persist.ril
getprop | grep persist.radio
```

### 2.3. Propiedades RIL (ril.*)

Propiedades temporales del RIL (Radio Interface Layer):

```bash
# Propiedades RIL temporales (se pierden al reiniciar)
setprop ril.sales_code OWO
setprop ril.matchedcsc OWO
setprop ril.official_cscver OWO16_0009

# Nota: Estas se restauran automáticamente desde EFS al reiniciar
```

---

## 🚀 PARTE 3: SERVICIOS A REINICIAR/DETENER

### 3.1. Servicios del Sistema

Lista completa de servicios a detener antes de modificar:

```bash
#!/system/bin/sh
# Detener servicios relacionados con CSC

# Servicios principales
stop rild
stop secril_config_svc
stop vendor.samsung.hardware.radio-service

# Servicios de telephony
am force-stop com.android.phone
am force-stop com.android.providers.telephony
am force-stop com.sec.phone

# Servicios CSC y CIDManager
am force-stop com.samsung.sec.android.application.csc
am force-stop com.samsung.android.cidmanager
am force-stop com.samsung.android.app.telephonyui

# Servicios IMS
am force-stop com.sec.imsservice
am force-stop com.samsung.ims

# Esperar a que los servicios se detengan
sleep 3
```

### 3.2. Servicios Vendor (Hardware)

```bash
# Detener servicios vendor de Samsung
stop vendor.samsung.hardware.radio-service
stop vendor.samsung.hardware.sehradio-service
stop vendor.qti.hardware.radio.qcrilhook-service
```

### 3.3. Reiniciar Servicios Después de Modificación

```bash
#!/system/bin/sh
# Reiniciar servicios después de modificar CSC

# Limpiar cachés primero
rm -rf /data/csc/*
rm -rf /cache/*
rm -rf /data/dalvik-cache/*

# Reiniciar servicios vendor
start vendor.samsung.hardware.radio-service
start vendor.samsung.hardware.sehradio-service

# Reiniciar rild
start secril_config_svc
sleep 2
start rild

# Reiniciar servicios de telephony
am start -n com.android.phone/.PhoneApp
am start -n com.samsung.sec.android.application.csc/.CSC

# Enviar broadcasts para activar cambios
am broadcast -a android.intent.action.SIM_STATE_CHANGED
am broadcast -a com.samsung.intent.action.CSC_UPDATE_TEST
am broadcast -a com.samsung.intent.action.CSC_COMPARE
```

---

## 📦 PARTE 4: BASES DE DATOS A MODIFICAR

### 4.1. Telephony Provider Database

```
Ubicación: /data/user_de/0/com.android.providers.telephony/databases/telephony.db
```

**Comandos SQL:**
```bash
# Usar sqlite3 para modificar
sqlite3 /data/user_de/0/com.android.providers.telephony/databases/telephony.db << EOF
-- Backup tabla
CREATE TABLE carriers_backup AS SELECT * FROM carriers;

-- Actualizar APNs para OWO (ejemplo)
UPDATE carriers SET numeric='310260' WHERE mcc='340';

-- Verificar cambios
SELECT * FROM carriers WHERE numeric='310260';
.quit
EOF

# Reiniciar proveedor
am force-stop com.android.providers.telephony
```

### 4.2. CIDManager Database

```
Ubicación: /data/user_de/0/com.samsung.sec.android.application.csc/databases/carrier.db
```

**Comandos:**
```bash
# Examinar base de datos
sqlite3 /data/user_de/0/com.samsung.sec.android.application.csc/databases/carrier.db ".schema"

# Limpiar caché de CIDManager
rm -rf /data/user_de/0/com.samsung.sec.android.application.csc/cache/*
rm -rf /data/user_de/0/com.samsung.sec.android.application.csc/shared_prefs/*
```

---

## 📂 PARTE 5: DIRECTORIOS Y CACHÉS

### 5.1. Directorios a Limpiar

```bash
#!/system/bin/sh
# Limpiar TODOS los cachés relacionados con CSC

# CSC caché principal
rm -rf /data/csc/*
rm -rf /data/sec_csc/*

# CIDManager
rm -rf /data/data/com.samsung.sec.android.application.csc/cache/*
rm -rf /data/data/com.samsung.sec.android.application.csc/shared_prefs/*
rm -rf /data/data/com.samsung.sec.android.application.csc/databases/*

# OMC caché
rm -rf /data/omc/TPA
rm -rf /data/omc/current

# Telephony
rm -rf /data/data/com.android.providers.telephony/cache/*

# Caché del sistema
rm -rf /cache/*
rm -rf /data/dalvik-cache/arm64/*
rm -rf /data/dalvik-cache/arm/*

# Logs
rm -rf /data/log/*
```

### 5.2. Crear Estructura OMC para OWO

```bash
#!/system/bin/sh
# Crear estructura OMC para OWO si no existe

mkdir -p /data/omc/OWO
mkdir -p /data/omc/OWO/conf
mkdir -p /data/omc/OWO/apps

# Copiar desde sistema si Multi-CSC está disponible
if [ -d /system/csc/OWO ]; then
    cp -r /system/csc/OWO/* /data/omc/OWO/
fi

# Crear symlink
rm -f /data/omc/current
ln -s /data/omc/OWO /data/omc/current

# Establecer propiedades
setprop persist.sys.omc_path /data/omc/OWO
setprop persist.sys.omc_root /system/csc/OWO
```

---

## 🔍 PARTE 6: ANÁLISIS DE BINARIOS (.so, .jar, .dex)

### 6.1. Librerías .so Críticas

#### libsec-ril.so (MÁS IMPORTANTE)

```
Ubicación: /vendor/lib64/libsec-ril.so
Tamaño: ~7 MB
Tipo: ELF 64-bit LSB shared object ARM aarch64
```

**Strings CSC encontrados:**
```
/efs/imei/mps_code.dat
%s/sales_code.dat
/efs/imei/replace_code.dat
/efs/imei/selective
persist.ril.matched_code
persist.ril.sales_network_code
ro.csc.sales_code
ro.csc.country_code
ro.csc.countryiso_code
```

**Dependencias:**
```
libril_sem.so
librilutils.so
libVendorSemTelephonyProps.so
libVendorSemDataProps.so
```

**Análisis con readelf:**
```bash
# Ver header
readelf -h /vendor/lib64/libsec-ril.so

# Ver dependencias
readelf -d /vendor/lib64/libsec-ril.so | grep NEEDED

# Ver símbolos
readelf -s /vendor/lib64/libsec-ril.so | grep -i csc

# Ver secciones
readelf -S /vendor/lib64/libsec-ril.so
```

**Análisis con strings:**
```bash
# Extraer todas las strings relacionadas con CSC
strings /vendor/lib64/libsec-ril.so | grep -E "sales|csc|efs|persist" > /sdcard/libsec-ril_strings.txt

# Buscar rutas de archivos
strings /vendor/lib64/libsec-ril.so | grep "/"  | grep -E "efs|data|system"

# Buscar propiedades
strings /vendor/lib64/libsec-ril.so | grep -E "ro\.|persist\.|ril\."
```

#### libVendorSemTelephonyProps.so

```
Ubicación: /vendor/lib64/libVendorSemTelephonyProps.so
```

**Propiedades manejadas:**
```
persist.radio.test_emer_num
persist.radio.support.dualrat
ril.deviceOffRes
ril.lteband
ro.ril.svdo
ro.ril.def_network_after_check_tdscdma
persist.radio.sat.sweepfreq
ril.sib16.last.timezone
persist.radio.def_network
persist.radio.multisim.config
ro.vendor.sec.radio.def_network
```

### 6.2. Archivos .jar

#### telephony-common.jar

```
Ubicación: /system/framework/telephony-common.jar
Contiene: classes.dex
```

**Análisis:**
```bash
# Extraer JAR
unzip /system/framework/telephony-common.jar -d /tmp/telephony-common/

# Analizar DEX
strings /tmp/telephony-common/classes.dex | grep -E "sales|csc" > /sdcard/telephony_strings.txt
```

#### framework.jar

```
Ubicación: /system/framework/framework.jar
```

**Nota:** Este JAR contiene el framework completo de Android. No tiene lógica específica de CSC de Samsung.

### 6.3. Archivos .dex

#### CIDManager classes.dex

**Análisis realizado:**
- 7658 clases smali
- Maneja persist.sys.sec_cid, persist.sys.sec_pcid
- Lee /efs/imei/sales_code.dat
- Clase SIMBasedChangeCSC para cambio automático

**Strings importantes extraídos:**
```
ro.csc.sales_code
ro.csc.countryiso_code  
ro.csc.country_code
persist.sys.sec_cid
persist.sys.sec_pcid
persist.sys.matched_code
persist.sys.omc_path
/efs/imei/mps_code.dat
sales_code.dat
```

#### TeleService classes.dex

**Tamaño:** 5.0 MB

**Análisis:**
```bash
# Extraer strings
strings /tmp/TeleService_extracted/classes.dex | grep -iE "sales|csc|efs"
```

---

## 💻 PARTE 7: COMANDOS SHELL COMPLETOS

### 7.1. Script Master de Modificación CSC

```bash
#!/system/bin/sh
# CSC_MASTER_CHANGE.sh
# Modificación COMPLETA de CSC TPA→OWO
# Requiere ROOT

set -e

TARGET_CSC="OWO"
BACKUP_DIR="/sdcard/CSC_BACKUP_MASTER_$(date +%Y%m%d_%H%M%S)"

echo "════════════════════════════════════════════"
echo "  MODIFICACIÓN MASTER CSC: TPA → $TARGET_CSC"
echo "════════════════════════════════════════════"

# ========================================
# FASE 0: Verificación
# ========================================
if [ "$(id -u)" -ne 0 ]; then
    echo "❌ ERROR: Se requiere ROOT"
    exit 1
fi

mkdir -p "$BACKUP_DIR"

# ========================================
# FASE 1: Detener Servicios
# ========================================
echo ""
echo "FASE 1: Deteniendo servicios..."
stop rild
stop secril_config_svc
am force-stop com.android.phone
am force-stop com.android.providers.telephony
am force-stop com.samsung.sec.android.application.csc
am force-stop com.samsung.android.cidmanager
sleep 3
echo "✓ Servicios detenidos"

# ========================================
# FASE 2: Backup Completo
# ========================================
echo ""
echo "FASE 2: Backup completo..."

# EFS
dd if=/dev/block/by-name/efs of="$BACKUP_DIR/efs.img" bs=4096 2>/dev/null
cp /efs/imei/mps_code.dat "$BACKUP_DIR/" 2>/dev/null
cp /efs/imei/sales_code.dat "$BACKUP_DIR/" 2>/dev/null

# Build.prop
cp /system/build.prop "$BACKUP_DIR/system_build.prop"
cp /vendor/build.prop "$BACKUP_DIR/vendor_build.prop"
cp /mnt/vendor/efs/telephony.prop "$BACKUP_DIR/telephony.prop" 2>/dev/null

# Propiedades
getprop > "$BACKUP_DIR/all_props.txt"

echo "✓ Backup completado: $BACKUP_DIR"

# ========================================
# FASE 3: Modificar EFS
# ========================================
echo ""
echo "FASE 3: Modificando EFS..."

mount -o remount,rw /efs

# Modificar archivos EFS
echo "$TARGET_CSC" > /efs/imei/mps_code.dat
echo "$TARGET_CSC" > /efs/imei/sales_code.dat
echo "$TARGET_CSC" > /efs/imei/replace_code.dat 2>/dev/null || true

# Permisos
chown radio:radio /efs/imei/mps_code.dat
chown radio:radio /efs/imei/sales_code.dat
chmod 0644 /efs/imei/mps_code.dat
chmod 0644 /efs/imei/sales_code.dat

sync
mount -o remount,ro /efs

echo "✓ EFS: mps_code=$(cat /efs/imei/mps_code.dat)"

# ========================================
# FASE 4: Modificar Vendor EFS
# ========================================
echo ""
echo "FASE 4: Modificando /mnt/vendor/efs..."

if [ -f /mnt/vendor/efs/telephony.prop ]; then
    sed -i 's/ro.csc.sales_code=.*/ro.csc.sales_code='$TARGET_CSC'/' /mnt/vendor/efs/telephony.prop
    sed -i 's/ril.sales_code=.*/ril.sales_code='$TARGET_CSC'/' /mnt/vendor/efs/telephony.prop
    
    # Agregar si no existe
    grep -q "ro.csc.sales_code" /mnt/vendor/efs/telephony.prop || \
        echo "ro.csc.sales_code=$TARGET_CSC" >> /mnt/vendor/efs/telephony.prop
    
    echo "✓ telephony.prop modificado"
fi

# ========================================
# FASE 5: Modificar build.prop
# ========================================
echo ""
echo "FASE 5: Modificando build.prop..."

mount -o remount,rw /
mount -o remount,rw /system
mount -o remount,rw /vendor

# Función para modificar build.prop
modify_prop() {
    local file="$1"
    if [ -f "$file" ]; then
        sed -i '/ro.csc.sales_code=/d' "$file"
        sed -i '/persist.sys.sec_cid=/d' "$file"
        echo "" >> "$file"
        echo "# CSC Modified" >> "$file"
        echo "ro.csc.sales_code=$TARGET_CSC" >> "$file"
        echo "persist.sys.sec_cid=$TARGET_CSC" >> "$file"
    fi
}

modify_prop /system/build.prop
modify_prop /vendor/build.prop

sync
mount -o remount,ro /system
mount -o remount,ro /vendor
mount -o remount,ro /

echo "✓ build.prop modificados"

# ========================================
# FASE 6: Propiedades Persist
# ========================================
echo ""
echo "FASE 6: Estableciendo propiedades persist..."

setprop persist.sys.sec_cid "$TARGET_CSC"
setprop persist.sys.sec_pcid "$TARGET_CSC"
setprop persist.sys.matched_code "$TARGET_CSC"
setprop persist.sys.omc_path "/system/csc/$TARGET_CSC"
setprop persist.sys.omc_root "/system/csc/$TARGET_CSC"
setprop persist.ril.matched_code "$TARGET_CSC"
setprop ril.sales_code "$TARGET_CSC"
setprop ril.matchedcsc "$TARGET_CSC"

echo "✓ Propiedades establecidas"

# ========================================
# FASE 7: Limpiar Cachés
# ========================================
echo ""
echo "FASE 7: Limpiando cachés..."

rm -rf /data/csc/*
rm -rf /data/sec_csc/*
rm -rf /data/data/com.samsung.sec.android.application.csc/cache/*
rm -rf /data/data/com.samsung.sec.android.application.csc/shared_prefs/*
rm -rf /data/omc/TPA
rm -rf /cache/*

echo "✓ Cachés limpiados"

# ========================================
# FASE 8: Crear estructura OMC
# ========================================
echo ""
echo "FASE 8: Configurando OMC..."

mkdir -p /data/omc/$TARGET_CSC
if [ -d /system/csc/$TARGET_CSC ]; then
    cp -r /system/csc/$TARGET_CSC/* /data/omc/$TARGET_CSC/
fi
rm -f /data/omc/current
ln -s /data/omc/$TARGET_CSC /data/omc/current

echo "✓ OMC configurado"

# ========================================
# FASE 9: Reiniciar Servicios
# ========================================
echo ""
echo "FASE 9: Reiniciando servicios..."

start secril_config_svc
sleep 2
start rild
sleep 2

# Broadcasts
am broadcast -a android.intent.action.SIM_STATE_CHANGED 2>/dev/null
am broadcast -a com.samsung.intent.action.CSC_UPDATE_TEST 2>/dev/null

echo "✓ Servicios reiniciados"

# ========================================
# FASE 10: Verificación
# ========================================
echo ""
echo "FASE 10: Verificación..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "EFS:"
echo "  mps_code.dat: $(cat /efs/imei/mps_code.dat)"
echo "  sales_code.dat: $(cat /efs/imei/sales_code.dat)"
echo ""
echo "Propiedades:"
echo "  persist.sys.sec_cid: $(getprop persist.sys.sec_cid)"
echo "  persist.ril.matched_code: $(getprop persist.ril.matched_code)"
echo "  ril.sales_code: $(getprop ril.sales_code)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ========================================
# FINALIZACIÓN
# ========================================
echo ""
echo "════════════════════════════════════════════"
echo "  ✓ MODIFICACIÓN COMPLETADA"
echo "════════════════════════════════════════════"
echo ""
echo "SIGUIENTE PASO:"
echo "  1. Reiniciar dispositivo: reboot"
echo "  2. Verificar CSC después de boot"
echo "  3. Si no cambia, hacer Factory Reset"
echo ""
echo "BACKUP: $BACKUP_DIR"
echo ""
```

### 7.2. Script de Verificación Post-Modificación

```bash
#!/system/bin/sh
# CSC_VERIFY.sh - Verificación completa después de modificar CSC

echo "════════════════════════════════════════════"
echo "  VERIFICACIÓN POST-MODIFICACIÓN CSC"
echo "════════════════════════════════════════════"

# Función de verificación
check_item() {
    local item="$1"
    local expected="$2"
    local actual="$3"
    
    if [ "$actual" = "$expected" ]; then
        echo "  ✓ $item: $actual"
        return 0
    else
        echo "  ✗ $item: $actual (esperado: $expected)"
        return 1
    fi
}

TARGET="OWO"
PASS=0
FAIL=0

echo ""
echo "【 ARCHIVOS EFS 】"
if [ "$(id -u)" -eq 0 ]; then
    if check_item "mps_code.dat" "$TARGET" "$(cat /efs/imei/mps_code.dat 2>/dev/null)"; then
        PASS=$((PASS+1))
    else
        FAIL=$((FAIL+1))
    fi
    
    if check_item "sales_code.dat" "$TARGET" "$(cat /efs/imei/sales_code.dat 2>/dev/null)"; then
        PASS=$((PASS+1))
    else
        FAIL=$((FAIL+1))
    fi
fi

echo ""
echo "【 PROPIEDADES PERSIST 】"
if check_item "persist.sys.sec_cid" "$TARGET" "$(getprop persist.sys.sec_cid)"; then
    PASS=$((PASS+1))
else
    FAIL=$((FAIL+1))
fi

if check_item "persist.ril.matched_code" "$TARGET" "$(getprop persist.ril.matched_code)"; then
    PASS=$((PASS+1))
else
    FAIL=$((FAIL+1))
fi

echo ""
echo "【 PROPIEDADES RIL 】"
if check_item "ril.sales_code" "$TARGET" "$(getprop ril.sales_code)"; then
    PASS=$((PASS+1))
else
    FAIL=$((FAIL+1))
fi

echo ""
echo "【 SERVICIOS 】"
if pgrep -f rild > /dev/null; then
    echo "  ✓ rild: Running"
    PASS=$((PASS+1))
else
    echo "  ✗ rild: Not running"
    FAIL=$((FAIL+1))
fi

if pgrep -f secril_config_svc > /dev/null; then
    echo "  ✓ secril_config_svc: Running"
    PASS=$((PASS+1))
else
    echo "  ✗ secril_config_svc: Not running"
    FAIL=$((FAIL+1))
fi

echo ""
echo "════════════════════════════════════════════"
echo "  RESULTADO: $PASS Passed, $FAIL Failed"
echo "════════════════════════════════════════════"

if [ $FAIL -gt 0 ]; then
    echo ""
    echo "⚠ Algunas verificaciones fallaron."
    echo "Considere:"
    echo "  1. Reiniciar el dispositivo"
    echo "  2. Ejecutar script de modificación nuevamente"
    echo "  3. Hacer Factory Reset (último recurso)"
fi

echo ""
```

---

## 📊 PARTE 8: ANÁLISIS DE init.rc

### 8.1. init.dm2q.rc - Lógica de CSC

```
Ubicación: /vendor/etc/init/hw/init.dm2q.rc
```

**CSCs configurados en init.rc:**
- DSA (Dish)
- DSG (Dish)
- DSH (Dish)
- ASR (US Cellular)
- TMK (T-Mobile)
- TMB (T-Mobile)

**Lógica:**
El init.rc monta directorios específicos según el `ro.csc.sales_code` durante el boot. Si OWO no está en la lista, el sistema usará configuración predeterminada.

---

## ✅ PARTE 9: CHECKLIST DE VERIFICACIÓN

### Pre-Modificación
- [ ] Backup completo de EFS (`dd if=/dev/block/by-name/efs`)
- [ ] Backup de build.prop files
- [ ] Root verificado y funcional
- [ ] ADB habilitado y funcional
- [ ] Batería > 50%
- [ ] Firmware stock descargado (plan B)

### Durante Modificación
- [ ] Servicios detenidos correctamente
- [ ] EFS modificado y verificado
- [ ] telephony.prop modificado
- [ ] build.prop modificados
- [ ] Propiedades persist establecidas
- [ ] Cachés limpiados
- [ ] Servicios reiniciados

### Post-Modificación
- [ ] Archivos EFS verificados
- [ ] Propiedades verificadas
- [ ] Servicios corriendo
- [ ] Sin errores en logcat
- [ ] Dispositivo reiniciado
- [ ] CSC cambiado exitosamente

### Si Falla
- [ ] Restaurar backup de EFS
- [ ] Restaurar build.prop
- [ ] Factory Reset
- [ ] Flash firmware stock via Odin

---

## 🔍 PARTE 10: COMANDOS DE DIAGNÓSTICO

```bash
#!/system/bin/sh
# Diagnóstico completo del sistema CSC

echo "═══════════════════════════════════════"
echo "  DIAGNÓSTICO COMPLETO CSC"
echo "═══════════════════════════════════════"

# Información del dispositivo
echo ""
echo "【 DEVICE INFO 】"
echo "Model: $(getprop ro.product.model)"
echo "Build: $(getprop ro.build.display.id)"
echo "Kernel: $(uname -r)"

# Todas las propiedades CSC
echo ""
echo "【 PROPIEDADES CSC 】"
getprop | grep -E "csc|sales|ril\.|persist\.sys\.(sec_|omc|matched)" | sort

# Estado de particiones
echo ""
echo "【 PARTICIONES 】"
mount | grep -E "efs|system|vendor"

# Servicios activos
echo ""
echo "【 SERVICIOS ACTIVOS 】"
ps -A | grep -E "rild|secril|phone|csc|cidmanager"

# Logs recientes
echo ""
echo "【 LOGS CSC (últimas 50 líneas) 】"
logcat -d -b all | grep -iE "csc|sales_code|cidmanager" | tail -50

echo ""
echo "═══════════════════════════════════════"
```

---

## 📝 NOTAS FINALES

### Archivos Más Críticos (Orden de Importancia)

1. `/efs/imei/mps_code.dat` - **CRÍTICO**
2. `/efs/imei/sales_code.dat` - **CRÍTICO**
3. `/mnt/vendor/efs/telephony.prop` - **MUY IMPORTANTE**
4. `/system/build.prop` - **IMPORTANTE**
5. `persist.sys.sec_cid` - **IMPORTANTE**
6. `/vendor/build.prop` - **RECOMENDADO**

### Binarios Más Importantes

1. `/vendor/lib64/libsec-ril.so` - Contiene toda la lógica RIL
2. `/vendor/bin/secril_config_svc` - Configura RIL al boot
3. `/vendor/bin/hw/rild` - Daemon del RIL
4. `/vendor/lib64/libVendorSemTelephonyProps.so` - Propiedades Samsung

### Comandos Esenciales

```bash
# Modificar CSC mínimo
echo "OWO" > /efs/imei/mps_code.dat
setprop persist.sys.sec_cid OWO
reboot

# Verificar CSC
getprop ro.csc.sales_code
cat /efs/imei/mps_code.dat

# Restaurar desde backup
dd if=/sdcard/efs_backup.img of=/dev/block/by-name/efs
```

---

**Versión:** 2.0  
**Fecha:** 2024-12-28  
**Dispositivo:** Samsung Galaxy S23+ (SM-S916B)  
**Firmware:** dm2q
