# Guía Paso a Paso Completa: Cambio Total de CSC TPA → OWO
## Cambio Completo de SAOMC_SM-S916B_OWO_TPA_16_0009 TPA/TPA,TPA/TPA a OWO/OWO,OWO/OWO

---

## 📋 Entendiendo el String CSC Completo

### Formato Actual
```
SAOMC_SM-S916B_OWO_TPA_16_0009 TPA/TPA,TPA/TPA
```

**Desglose:**
- `SAOMC` = Samsung Android Open Market Code
- `SM-S916B` = Modelo del dispositivo
- `OWO_TPA` = **CSC Activo/Original** (OWO primario, TPA secundario)
- `16_0009` = Versión del firmware
- `TPA/TPA` = **Active CSC / Installed CSC** (CSC activo / CSC instalado)
- `TPA/TPA` = **Home CSC / Carrier CSC** (CSC de inicio / CSC del operador)

### Formato Objetivo
```
SAOMC_SM-S916B_OWO_OWO_16_0009 OWO/OWO,OWO/OWO
```

**Cambios Necesarios:**
1. `OWO_TPA` → `OWO_OWO` (en el nombre del firmware)
2. Primera `TPA/TPA` → `OWO/OWO` (Active/Installed)
3. Segunda `TPA/TPA` → `OWO/OWO` (Home/Carrier)

---

## 🎯 PARTE 1: ANÁLISIS PROFUNDO DE ARCHIVOS

### 1.1. Archivos que Almacenan el String CSC Completo

#### A. `/efs/imei/` - Partición EFS (CRÍTICA)

```bash
# Localización de archivos
/efs/imei/mps_code.dat           # Multi-CSC Principal
/efs/imei/sales_code.dat         # Sales Code Activo
/efs/imei/replace_code.dat       # Código de reemplazo
/efs/imei/.csc_list              # Lista de CSC disponibles (si existe)
/efs/imei/cscfeature.xml         # Características del CSC (si existe)
```

**Análisis con `hexdump`:**
```bash
# Ver contenido hexadecimal de mps_code.dat
hexdump -C /efs/imei/mps_code.dat

# Ejemplo de salida:
# 00000000  54 50 41 0a              |TPA.|
# Muestra "TPA" seguido de newline (0x0a)
```

**Análisis con `strings`:**
```bash
# Extraer strings legibles
strings /efs/imei/mps_code.dat
# Salida: TPA

strings /efs/imei/sales_code.dat  
# Salida: TPA
```

#### B. `/mnt/vendor/efs/` - Vendor EFS

```bash
# Archivo crítico
/mnt/vendor/efs/telephony.prop
```

**Contenido típico:**
```properties
# Ejemplo de contenido
ro.csc.sales_code=TPA
ril.sales_code=TPA
persist.ril.matched_code=TPA
```

**Análisis:**
```bash
# Ver contenido completo
cat /mnt/vendor/efs/telephony.prop

# Buscar líneas con TPA
grep TPA /mnt/vendor/efs/telephony.prop
```

#### C. Build.prop Files - Propiedades del Sistema

```bash
# Archivos principales
/system/build.prop
/vendor/build.prop
/product/etc/build.prop
/odm/etc/build.prop
/system_ext/etc/build.prop
```

**Propiedades CSC en build.prop:**
```properties
# Ejemplo de /system/build.prop
ro.csc.sales_code=TPA
ro.csc.country_code=US
ro.csc.countryiso_code=US
ro.product.name=dm2qowotpa
ro.product.vendor.name=dm2qowotpa
persist.sys.sec_cid=TPA
```

**Análisis:**
```bash
# Buscar todas las referencias a TPA
grep -i tpa /system/build.prop
grep -i tpa /vendor/build.prop

# Buscar propiedades CSC
grep "ro.csc" /system/build.prop
grep "ro.product.name" /system/build.prop
```

#### D. Init Scripts - init.rc Files

```bash
# Archivos de inicialización
/vendor/etc/init/hw/init.dm2q.rc
/system/etc/init/*.rc
```

**Contenido relevante en init.dm2q.rc:**
```bash
# Ejemplo de sección CSC
on post-fs-data && property:ro.csc.sales_code=TPA
    # Comandos específicos para TPA
    mount none /system/carrier/TPA /system/carrier bind
```

**Análisis:**
```bash
# Buscar referencias a TPA en init scripts
grep -r "TPA" /vendor/etc/init/
grep -r "sales_code" /vendor/etc/init/hw/init.dm2q.rc
```

### 1.2. Archivos de Configuración Carrier

#### A. Directorio `/system/carrier/`

```bash
# Estructura típica
/system/carrier/TPA/              # Directorio específico de TPA
/system/carrier/TPA/app/          # Apps del carrier
/system/carrier/TPA/priv-app/     # Apps privilegiadas
/system/carrier/TPA/etc/          # Configuraciones
```

**Análisis:**
```bash
# Listar contenido
ls -la /system/carrier/TPA/

# Ver apps instaladas
find /system/carrier/TPA/ -name "*.apk"
```

#### B. Configuración OMC (Open Market Customization)

```bash
# Directorios OMC
/system/csc/TPA/              # CSC data de TPA
/data/omc/TPA/                # OMC runtime de TPA
/data/omc/current -> TPA      # Symlink al CSC actual
```

**Análisis:**
```bash
# Ver estructura OMC
ls -la /system/csc/
ls -la /data/omc/

# Ver symlink actual
readlink /data/omc/current
```

### 1.3. Bases de Datos SQLite

#### A. Telephony Database

```bash
# Ubicación
/data/user_de/0/com.android.providers.telephony/databases/telephony.db
```

**Análisis con sqlite3:**
```bash
# Abrir base de datos
sqlite3 /data/user_de/0/com.android.providers.telephony/databases/telephony.db

# Comandos SQL
.tables                              # Ver todas las tablas
.schema carriers                     # Ver estructura de tabla carriers
SELECT * FROM carriers WHERE mcc LIKE '3%';  # Ver carriers USA
SELECT * FROM carriers WHERE name LIKE '%TPA%';  # Buscar TPA
```

**Tablas importantes:**
- `carriers` - Configuración de APNs
- `siminfo` - Información de SIM
- `carrier_id` - IDs de carriers

#### B. CIDManager Database

```bash
# Ubicación
/data/user_de/0/com.samsung.sec.android.application.csc/databases/carrier.db
```

**Análisis:**
```bash
sqlite3 /data/user_de/0/com.samsung.sec.android.application.csc/databases/carrier.db

# Ver estructura
.tables
.schema
```

### 1.4. Binarios y Librerías

#### A. libsec-ril.so - RIL Principal

```bash
# Ubicación
/vendor/lib64/libsec-ril.so
```

**Análisis con readelf:**
```bash
# Ver información del binario
readelf -h /vendor/lib64/libsec-ril.so

# Ver dependencias
readelf -d /vendor/lib64/libsec-ril.so | grep NEEDED

# Ver símbolos
readelf -s /vendor/lib64/libsec-ril.so | grep -i csc
```

**Análisis con strings:**
```bash
# Extraer todas las strings
strings /vendor/lib64/libsec-ril.so > /sdcard/libsec-ril_strings.txt

# Buscar referencias CSC
strings /vendor/lib64/libsec-ril.so | grep -i "tpa\|csc\|sales"

# Ejemplo de salida:
# /efs/imei/mps_code.dat
# ro.csc.sales_code
# persist.ril.matched_code
```

**Análisis con nm (si está disponible):**
```bash
# Ver símbolos del binario
nm -D /vendor/lib64/libsec-ril.so | grep -i csc
```

#### B. secril_config_svc - Servicio de Configuración RIL

```bash
# Ubicación
/vendor/bin/secril_config_svc
```

**Análisis:**
```bash
# Tipo de archivo
file /vendor/bin/secril_config_svc

# Extraer strings
strings /vendor/bin/secril_config_svc | grep -E "efs|csc|tpa|sales"

# Ejemplo de salida:
# /mnt/vendor/efs/telephony.prop
# ro.csc.sales_code
# NetworkConfig: ro.csc.sales_code - %s
```

### 1.5. APKs y Smali Analysis

#### A. CIDManager.apk

**Ya decompilado en:** `/tmp/deep_analysis/CIDManager/`

**Clases clave en smali:**
```bash
# Clase que maneja sales_code
./smali/i/a.smali
    # const-string v0, "ro.csc.sales_code"
    # const-string p2, "ro.csc.countryiso_code"

# Clase de propiedades del sistema
./smali/c/a.smali
    # const-string p0, "persist.sys.sec_cid"
    # const-string p0, "persist.sys.sec_pcid"

# Clase SIMBasedChangeCSC
./smali/s/c.smali
    # const-string v1, "[SIMBasedChangeCSC] SIMBasedActivation ("
```

**Buscar referencias a TPA en smali:**
```bash
cd /tmp/deep_analysis/CIDManager
grep -r "TPA" ./smali --include="*.smali"
grep -r "\"TPA\"" ./smali --include="*.smali"
```

#### B. CSC.apk

**Ya decompilado en:** `/tmp/csc_analysis/CSC_decompiled/`

**Clases clave:**
```bash
# CSC Ringtone Manager
./smali/i/r.smali
    # const-string v0, "ro.csc.sales_code"

# CSC Compare Service
./smali/i/q.smali
    # const-string v6, "ro.csc.sales_code"
```

---

## 🔧 PARTE 2: PASOS DE MODIFICACIÓN DETALLADOS

### PASO 0: Preparación y Backup (OBLIGATORIO)

```bash
#!/system/bin/sh
# 0_preparacion.sh - Ejecutar como root

echo "═══════════════════════════════════════════════════"
echo " PASO 0: PREPARACIÓN Y BACKUP COMPLETO"
echo "═══════════════════════════════════════════════════"

# Verificar root
if [ "$(id -u)" -ne 0 ]; then
    echo "❌ ERROR: Se requiere ROOT"
    exit 1
fi

# Crear directorio de backup
BACKUP_DIR="/sdcard/CSC_FULL_BACKUP_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "📁 Directorio de backup: $BACKUP_DIR"

# 1. Backup COMPLETO de EFS (MÁS IMPORTANTE)
echo ""
echo "🔸 1. Backup de partición EFS..."
dd if=/dev/block/by-name/efs of="$BACKUP_DIR/efs_FULL.img" bs=4096
echo "✅ EFS backup: efs_FULL.img ($(du -h "$BACKUP_DIR/efs_FULL.img" | cut -f1))"

# 2. Backup de archivos EFS individuales
echo ""
echo "🔸 2. Backup de archivos EFS individuales..."
cp /efs/imei/mps_code.dat "$BACKUP_DIR/" 2>/dev/null
cp /efs/imei/sales_code.dat "$BACKUP_DIR/" 2>/dev/null
cp /efs/imei/replace_code.dat "$BACKUP_DIR/" 2>/dev/null
echo "   - mps_code.dat: $(cat /efs/imei/mps_code.dat 2>/dev/null || echo 'N/A')"
echo "   - sales_code.dat: $(cat /efs/imei/sales_code.dat 2>/dev/null || echo 'N/A')"

# 3. Backup de Vendor EFS
echo ""
echo "🔸 3. Backup de Vendor EFS..."
if [ -f /mnt/vendor/efs/telephony.prop ]; then
    cp /mnt/vendor/efs/telephony.prop "$BACKUP_DIR/"
    echo "✅ telephony.prop respaldado"
fi
if [ -f /mnt/vendor/efs/factory.prop ]; then
    cp /mnt/vendor/efs/factory.prop "$BACKUP_DIR/"
    echo "✅ factory.prop respaldado"
fi

# 4. Backup de build.prop files
echo ""
echo "🔸 4. Backup de build.prop files..."
cp /system/build.prop "$BACKUP_DIR/system_build.prop"
cp /vendor/build.prop "$BACKUP_DIR/vendor_build.prop"
cp /product/etc/build.prop "$BACKUP_DIR/product_build.prop" 2>/dev/null
cp /odm/etc/build.prop "$BACKUP_DIR/odm_build.prop" 2>/dev/null
echo "✅ build.prop files respaldados"

# 5. Backup de propiedades actuales
echo ""
echo "🔸 5. Backup de propiedades del sistema..."
getprop > "$BACKUP_DIR/all_properties.txt"
getprop | grep -i csc > "$BACKUP_DIR/csc_properties.txt"
getprop | grep sales > "$BACKUP_DIR/sales_properties.txt"
getprop | grep persist.sys > "$BACKUP_DIR/persist_properties.txt"
echo "✅ Propiedades respaldadas"

# 6. Backup de bases de datos
echo ""
echo "🔸 6. Backup de bases de datos..."
if [ -f /data/user_de/0/com.android.providers.telephony/databases/telephony.db ]; then
    cp /data/user_de/0/com.android.providers.telephony/databases/telephony.db "$BACKUP_DIR/"
    echo "✅ telephony.db respaldado"
fi
if [ -d /data/user_de/0/com.samsung.sec.android.application.csc/databases/ ]; then
    cp -r /data/user_de/0/com.samsung.sec.android.application.csc/databases/ "$BACKUP_DIR/csc_databases/"
    echo "✅ CIDManager databases respaldados"
fi

# 7. Información del sistema
echo ""
echo "🔸 7. Guardando información del sistema..."
cat > "$BACKUP_DIR/system_info.txt" << EOF
=== INFORMACIÓN DEL SISTEMA ===
Fecha: $(date)
Modelo: $(getprop ro.product.model)
Build: $(getprop ro.build.display.id)
Android: $(getprop ro.build.version.release)
Kernel: $(uname -r)

=== CSC ACTUAL ===
ro.csc.sales_code: $(getprop ro.csc.sales_code)
ril.sales_code: $(getprop ril.sales_code)
persist.sys.sec_cid: $(getprop persist.sys.sec_cid)
persist.sys.sec_pcid: $(getprop persist.sys.sec_pcid)

EFS:
mps_code.dat: $(cat /efs/imei/mps_code.dat 2>/dev/null || echo 'N/A')
sales_code.dat: $(cat /efs/imei/sales_code.dat 2>/dev/null || echo 'N/A')

=== PARTICIONES ===
$(mount | grep -E "efs|system|vendor")

=== SERVICIOS ACTIVOS ===
$(ps -A | grep -E "rild|secril|cidmanager|phone")
EOF
echo "✅ Información del sistema guardada"

# 8. Crear checksum
echo ""
echo "🔸 8. Generando checksums..."
cd "$BACKUP_DIR"
sha256sum * > checksums.txt 2>/dev/null
echo "✅ Checksums generados"

# Resumen final
echo ""
echo "═══════════════════════════════════════════════════"
echo " ✅ BACKUP COMPLETO FINALIZADO"
echo "═══════════════════════════════════════════════════"
echo ""
echo "📁 Ubicación: $BACKUP_DIR"
echo "📊 Archivos respaldados:"
ls -lh "$BACKUP_DIR"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   1. Copiar este backup a tu PC AHORA:"
echo "      adb pull $BACKUP_DIR"
echo "   2. Guardar en múltiples ubicaciones seguras"
echo "   3. NO continuar sin verificar que el backup está completo"
echo ""
echo "🔍 Para verificar backup:"
echo "   cat $BACKUP_DIR/checksums.txt"
echo ""
```

### PASO 1: Detener Todos los Servicios Relevantes

```bash
#!/system/bin/sh
# 1_detener_servicios.sh - Ejecutar como root

echo "═══════════════════════════════════════════════════"
echo " PASO 1: DETENER SERVICIOS"
echo "═══════════════════════════════════════════════════"

# Función para detener servicio y verificar
stop_service() {
    local service=$1
    echo "🔸 Deteniendo $service..."
    stop "$service" 2>/dev/null && echo "   ✅ $service detenido" || echo "   ℹ️  $service no se pudo detener o no existe"
}

# Función para detener app y verificar
stop_app() {
    local app=$1
    echo "🔸 Deteniendo app $app..."
    am force-stop "$app" 2>/dev/null && echo "   ✅ $app detenido" || echo "   ℹ️  $app no se pudo detener"
}

echo ""
echo "📱 Deteniendo servicios vendor..."
stop_service vendor.samsung.hardware.radio-service
stop_service vendor.samsung.hardware.sehradio-service
stop_service vendor.qti.hardware.radio.qcrilhook-service

echo ""
echo "📱 Deteniendo servicios RIL..."
stop_service rild
stop_service secril_config_svc

echo ""
echo "📱 Deteniendo aplicaciones telephony..."
stop_app com.android.phone
stop_app com.android.providers.telephony
stop_app com.sec.phone

echo ""
echo "📱 Deteniendo aplicaciones CSC y CIDManager..."
stop_app com.samsung.sec.android.application.csc
stop_app com.samsung.android.cidmanager
stop_app com.samsung.android.app.telephonyui

echo ""
echo "📱 Deteniendo servicios IMS..."
stop_app com.sec.imsservice
stop_app com.samsung.ims

echo ""
echo "⏳ Esperando 5 segundos para que se detengan completamente..."
sleep 5

echo ""
echo "🔍 Verificando servicios detenidos..."
ps -A | grep -E "rild|secril|phone|csc|cidmanager|ims" || echo "✅ Todos los servicios detenidos correctamente"

echo ""
echo "═══════════════════════════════════════════════════"
echo " ✅ SERVICIOS DETENIDOS"
echo "═══════════════════════════════════════════════════"
```

### PASO 2: Modificar Partición EFS

```bash
#!/system/bin/sh
# 2_modificar_efs.sh - Ejecutar como root

TARGET_CSC="OWO"

echo "═══════════════════════════════════════════════════"
echo " PASO 2: MODIFICAR PARTICIÓN EFS"
echo "═══════════════════════════════════════════════════"
echo "🎯 Objetivo: Cambiar de TPA a $TARGET_CSC"
echo ""

# Remontar EFS como RW
echo "🔸 Remontando EFS como lectura-escritura..."
mount -o remount,rw /efs
if [ $? -eq 0 ]; then
    echo "✅ EFS remontado como RW"
else
    echo "❌ ERROR: No se pudo remontar EFS"
    exit 1
fi

# Ver estado actual
echo ""
echo "📊 Estado ANTES de modificar:"
echo "   mps_code.dat: $(cat /efs/imei/mps_code.dat 2>/dev/null || echo 'No existe')"
echo "   sales_code.dat: $(cat /efs/imei/sales_code.dat 2>/dev/null || echo 'No existe')"
echo "   replace_code.dat: $(cat /efs/imei/replace_code.dat 2>/dev/null || echo 'No existe')"

# Modificar mps_code.dat
echo ""
echo "🔸 Modificando /efs/imei/mps_code.dat..."
echo "$TARGET_CSC" > /efs/imei/mps_code.dat
chown radio:radio /efs/imei/mps_code.dat
chmod 0644 /efs/imei/mps_code.dat
echo "✅ mps_code.dat modificado"

# Modificar sales_code.dat
echo "🔸 Modificando /efs/imei/sales_code.dat..."
echo "$TARGET_CSC" > /efs/imei/sales_code.dat
chown radio:radio /efs/imei/sales_code.dat
chmod 0644 /efs/imei/sales_code.dat
echo "✅ sales_code.dat modificado"

# Modificar replace_code.dat (si existe)
echo "🔸 Modificando /efs/imei/replace_code.dat..."
echo "$TARGET_CSC" > /efs/imei/replace_code.dat 2>/dev/null
chown radio:radio /efs/imei/replace_code.dat 2>/dev/null
chmod 0644 /efs/imei/replace_code.dat 2>/dev/null
echo "✅ replace_code.dat modificado (o creado)"

# Sincronizar cambios
echo ""
echo "💾 Sincronizando cambios al disco..."
sync
sleep 2
echo "✅ Cambios sincronizados"

# Remontar como RO
echo ""
echo "🔸 Remontando EFS como solo-lectura..."
mount -o remount,ro /efs
echo "✅ EFS remontado como RO"

# Verificar cambios
echo ""
echo "📊 Estado DESPUÉS de modificar:"
echo "   mps_code.dat: $(cat /efs/imei/mps_code.dat)"
echo "   sales_code.dat: $(cat /efs/imei/sales_code.dat)"
echo "   replace_code.dat: $(cat /efs/imei/replace_code.dat 2>/dev/null || echo 'N/A')"

echo ""
echo "🔍 Verificando permisos:"
ls -la /efs/imei/mps_code.dat
ls -la /efs/imei/sales_code.dat

echo ""
echo "═══════════════════════════════════════════════════"
echo " ✅ EFS MODIFICADO EXITOSAMENTE"
echo "═══════════════════════════════════════════════════"
```

### PASO 3: Modificar Vendor EFS (telephony.prop)

```bash
#!/system/bin/sh
# 3_modificar_vendor_efs.sh - Ejecutar como root

TARGET_CSC="OWO"

echo "═══════════════════════════════════════════════════"
echo " PASO 3: MODIFICAR VENDOR EFS"
echo "═══════════════════════════════════════════════════"

# Verificar si existe telephony.prop
if [ ! -f /mnt/vendor/efs/telephony.prop ]; then
    echo "ℹ️  telephony.prop no existe, creando..."
    touch /mnt/vendor/efs/telephony.prop
fi

# Backup del archivo original
echo "💾 Creando backup..."
cp /mnt/vendor/efs/telephony.prop /mnt/vendor/efs/telephony.prop.bak

# Mostrar contenido actual
echo ""
echo "📄 Contenido ANTES:"
cat /mnt/vendor/efs/telephony.prop

# Modificar o agregar propiedades
echo ""
echo "🔸 Modificando telephony.prop..."

# Función para modificar o agregar propiedad
modify_prop() {
    local key=$1
    local value=$2
    local file=$3
    
    if grep -q "^${key}=" "$file"; then
        # Modificar existente
        sed -i "s|^${key}=.*|${key}=${value}|" "$file"
    else
        # Agregar nueva
        echo "${key}=${value}" >> "$file"
    fi
}

# Modificar propiedades CSC
modify_prop "ro.csc.sales_code" "$TARGET_CSC" /mnt/vendor/efs/telephony.prop
modify_prop "ril.sales_code" "$TARGET_CSC" /mnt/vendor/efs/telephony.prop
modify_prop "persist.ril.matched_code" "$TARGET_CSC" /mnt/vendor/efs/telephony.prop
modify_prop "persist.sys.sec_cid" "$TARGET_CSC" /mnt/vendor/efs/telephony.prop

# Establecer permisos correctos
chown radio:radio /mnt/vendor/efs/telephony.prop
chmod 0644 /mnt/vendor/efs/telephony.prop

# Sincronizar
sync
sleep 1

# Mostrar contenido modificado
echo ""
echo "📄 Contenido DESPUÉS:"
cat /mnt/vendor/efs/telephony.prop

echo ""
echo "🔍 Verificando permisos:"
ls -la /mnt/vendor/efs/telephony.prop

echo ""
echo "═══════════════════════════════════════════════════"
echo " ✅ VENDOR EFS MODIFICADO"
echo "═══════════════════════════════════════════════════"
```

### PASO 4: Modificar Build.prop Files

```bash
#!/system/bin/sh
# 4_modificar_buildprop.sh - Ejecutar como root

TARGET_CSC="OWO"

echo "═══════════════════════════════════════════════════"
echo " PASO 4: MODIFICAR BUILD.PROP FILES"
echo "═══════════════════════════════════════════════════"

# Función para modificar build.prop
modify_buildprop() {
    local file=$1
    local backup="${file}.bak_$(date +%Y%m%d)"
    
    if [ ! -f "$file" ]; then
        echo "⚠️  $file no existe, saltando..."
        return
    fi
    
    echo ""
    echo "🔸 Modificando $file..."
    
    # Backup
    cp "$file" "$backup"
    echo "   💾 Backup: $backup"
    
    # Función auxiliar para modificar o agregar
    modify_or_add() {
        local prop=$1
        local value=$2
        local file=$3
        
        if grep -q "^${prop}=" "$file"; then
            sed -i "s|^${prop}=.*|${prop}=${value}|" "$file"
            echo "   ✏️  Modificado: ${prop}=${value}"
        else
            echo "" >> "$file"
            echo "${prop}=${value}" >> "$file"
            echo "   ➕ Agregado: ${prop}=${value}"
        fi
    }
    
    # Remover líneas viejas que puedan causar conflicto
    sed -i '/^ro.csc.sales_code=/d' "$file"
    sed -i '/^persist.sys.sec_cid=/d' "$file"
    sed -i '/^persist.sys.sec_pcid=/d' "$file"
    sed -i '/^ril.sales_code=/d' "$file"
    
    # Agregar sección CSC
    echo "" >> "$file"
    echo "# === CSC Configuration Modified to $TARGET_CSC ===" >> "$file"
    echo "ro.csc.sales_code=$TARGET_CSC" >> "$file"
    echo "persist.sys.sec_cid=$TARGET_CSC" >> "$file"
    echo "persist.sys.sec_pcid=$TARGET_CSC" >> "$file"
    echo "ril.sales_code=$TARGET_CSC" >> "$file"
    
    # Modificar ro.product.name si contiene TPA
    if grep -q "^ro.product.name=.*tpa" "$file"; then
        sed -i "s|tpa|owo|g" "$file"
        echo "   ✏️  ro.product.name modificado (tpa → owo)"
    fi
    
    # Modificar ro.product.vendor.name si contiene TPA
    if grep -q "^ro.product.vendor.name=.*tpa" "$file"; then
        sed -i "s|tpa|owo|g" "$file"
        echo "   ✏️  ro.product.vendor.name modificado (tpa → owo)"
    fi
    
    sync
    echo "   ✅ $file modificado exitosamente"
}

# Remontar particiones como RW
echo "🔸 Remontando particiones como RW..."
mount -o remount,rw /
mount -o remount,rw /system
mount -o remount,rw /vendor
mount -o remount,rw /product
mount -o remount,rw /odm
echo "✅ Particiones remontadas"

# Modificar cada build.prop
modify_buildprop /system/build.prop
modify_buildprop /vendor/build.prop
modify_buildprop /product/etc/build.prop
modify_buildprop /odm/etc/build.prop
modify_buildprop /system_ext/etc/build.prop

# Sincronizar todos los cambios
echo ""
echo "💾 Sincronizando todos los cambios..."
sync
sleep 2
echo "✅ Cambios sincronizados"

# Remontar como RO
echo ""
echo "🔸 Remontando particiones como RO..."
mount -o remount,ro /system
mount -o remount,ro /vendor
mount -o remount,ro /product
mount -o remount,ro /odm
mount -o remount,ro /
echo "✅ Particiones protegidas"

echo ""
echo "═══════════════════════════════════════════════════"
echo " ✅ BUILD.PROP FILES MODIFICADOS"
echo "═══════════════════════════════════════════════════"
```

### PASO 5: Establecer Propiedades Persist

```bash
#!/system/bin/sh
# 5_establecer_propiedades.sh - Ejecutar como root

TARGET_CSC="OWO"

echo "═══════════════════════════════════════════════════"
echo " PASO 5: ESTABLECER PROPIEDADES PERSIST"
echo "═══════════════════════════════════════════════════"

# Función para establecer y verificar propiedad
set_and_verify() {
    local prop=$1
    local value=$2
    
    echo "🔸 Estableciendo $prop..."
    setprop "$prop" "$value"
    sleep 0.5
    
    local actual=$(getprop "$prop")
    if [ "$actual" = "$value" ]; then
        echo "   ✅ $prop = $actual"
        return 0
    else
        echo "   ⚠️  $prop = $actual (esperado: $value)"
        return 1
    fi
}

echo ""
echo "📱 Propiedades CSC Core:"
set_and_verify "persist.sys.sec_cid" "$TARGET_CSC"
set_and_verify "persist.sys.sec_pcid" "$TARGET_CSC"
set_and_verify "persist.sys.sec_operator" "$TARGET_CSC"
set_and_verify "persist.sys.matched_code" "$TARGET_CSC"
set_and_verify "persist.sys.sec_cid_ver" "16_0009"

echo ""
echo "📱 Propiedades OMC (Open Market Customization):"
set_and_verify "persist.sys.omc_path" "/system/csc/$TARGET_CSC"
set_and_verify "persist.sys.omc_root" "/system/csc/$TARGET_CSC"
set_and_verify "persist.sys.omc_support" "true"
set_and_verify "persist.sys.omcnw_path" "/data/omc/$TARGET_CSC"

echo ""
echo "📱 Propiedades RIL (Radio Interface Layer):"
set_and_verify "persist.ril.matched_code" "$TARGET_CSC"
set_and_verify "persist.ril.sales_network_code" "$TARGET_CSC"

echo ""
echo "📱 Propiedades Radio:"
set_and_verify "persist.radio.def_network" "33"
set_and_verify "persist.radio.multisim.config" "dsds"

echo ""
echo "📱 Propiedades RIL Temporales (se perderán al reiniciar):"
setprop "ril.sales_code" "$TARGET_CSC"
setprop "ril.matchedcsc" "$TARGET_CSC"
setprop "ril.official_cscver" "${TARGET_CSC}16_0009"
echo "   ✅ Propiedades RIL temporales establecidas"

echo ""
echo "🔍 Resumen de propiedades establecidas:"
getprop | grep "persist.sys.sec" | grep -E "cid|operator|matched"
getprop | grep "persist.sys.omc"
getprop | grep "persist.ril"
getprop | grep "persist.radio" | grep -E "def_network|multisim"

echo ""
echo "═══════════════════════════════════════════════════"
echo " ✅ PROPIEDADES ESTABLECIDAS"
echo "═══════════════════════════════════════════════════"
```

### PASO 6: Limpiar Cachés y Datos

```bash
#!/system/bin/sh
# 6_limpiar_caches.sh - Ejecutar como root

echo "═══════════════════════════════════════════════════"
echo " PASO 6: LIMPIAR CACHÉS Y DATOS"
echo "═══════════════════════════════════════════════════"

# Función para limpiar directorio
clean_dir() {
    local dir=$1
    local desc=$2
    
    if [ -d "$dir" ]; then
        echo "🗑️  Limpiando $desc..."
        rm -rf "$dir"/* 2>/dev/null
        echo "   ✅ $desc limpiado"
        return 0
    else
        echo "   ℹ️  $desc no existe"
        return 1
    fi
}

echo ""
echo "📂 Limpiando cachés CSC:"
clean_dir "/data/csc" "CSC cache principal"
clean_dir "/data/sec_csc" "SEC CSC cache"

echo ""
echo "📂 Limpiando CIDManager:"
clean_dir "/data/data/com.samsung.sec.android.application.csc/cache" "CIDManager cache"
clean_dir "/data/data/com.samsung.sec.android.application.csc/shared_prefs" "CIDManager prefs"
clean_dir "/data/user_de/0/com.samsung.sec.android.application.csc/cache" "CIDManager cache (DE)"
clean_dir "/data/user_de/0/com.samsung.sec.android.application.csc/shared_prefs" "CIDManager prefs (DE)"

echo ""
echo "📂 Limpiando OMC:"
clean_dir "/data/omc/TPA" "OMC TPA"
if [ -L /data/omc/current ]; then
    echo "🔗 Removiendo symlink /data/omc/current..."
    rm -f /data/omc/current
    echo "   ✅ Symlink removido"
fi

echo ""
echo "📂 Limpiando Telephony Provider:"
clean_dir "/data/data/com.android.providers.telephony/cache" "Telephony cache"
clean_dir "/data/user_de/0/com.android.providers.telephony/cache" "Telephony cache (DE)"

echo ""
echo "📂 Limpiando Phone app:"
clean_dir "/data/data/com.android.phone/cache" "Phone cache"
clean_dir "/data/user_de/0/com.android.phone/cache" "Phone cache (DE)"

echo ""
echo "📂 Limpiando caché del sistema:"
clean_dir "/cache" "System cache"
clean_dir "/data/dalvik-cache/arm64" "Dalvik cache ARM64"
clean_dir "/data/dalvik-cache/arm" "Dalvik cache ARM"

echo ""
echo "📂 Limpiando logs:"
clean_dir "/data/log" "System logs"
clean_dir "/data/vendor/log" "Vendor logs"

echo ""
echo "💾 Sincronizando cambios..."
sync
sleep 2
echo "✅ Cambios sincronizados"

echo ""
echo "═══════════════════════════════════════════════════"
echo " ✅ CACHÉS LIMPIADOS"
echo "═══════════════════════════════════════════════════"
```

### PASO 7: Configurar OMC para OWO

```bash
#!/system/bin/sh
# 7_configurar_omc.sh - Ejecutar como root

TARGET_CSC="OWO"

echo "═══════════════════════════════════════════════════"
echo " PASO 7: CONFIGURAR OMC (Open Market Customization)"
echo "═══════════════════════════════════════════════════"

# Crear estructura OMC
echo "🔸 Creando estructura OMC para $TARGET_CSC..."
mkdir -p /data/omc/$TARGET_CSC
mkdir -p /data/omc/$TARGET_CSC/conf
mkdir -p /data/omc/$TARGET_CSC/apps
mkdir -p /data/omc/$TARGET_CSC/etc
echo "✅ Estructura creada"

# Copiar desde sistema si Multi-CSC está disponible
echo ""
echo "🔸 Buscando Multi-CSC en /system/csc/..."
if [ -d /system/csc/$TARGET_CSC ]; then
    echo "   ✅ Multi-CSC $TARGET_CSC encontrado en sistema"
    echo "   📋 Copiando archivos..."
    cp -r /system/csc/$TARGET_CSC/* /data/omc/$TARGET_CSC/ 2>/dev/null
    echo "   ✅ Archivos copiados"
elif [ -d /system/csc ]; then
    echo "   ℹ️  Directorio /system/csc existe pero no contiene $TARGET_CSC"
    echo "   📋 CSC disponibles:"
    ls -1 /system/csc/
    
    # Intentar copiar de OWO si existe
    if [ -d /system/csc/OWO ]; then
        echo "   📋 Copiando desde /system/csc/OWO..."
        cp -r /system/csc/OWO/* /data/omc/$TARGET_CSC/ 2>/dev/null
    fi
else
    echo "   ℹ️  No se encontró Multi-CSC en el sistema"
    echo "   ℹ️  Se usará configuración por defecto"
fi

# Crear symlink
echo ""
echo "🔸 Creando symlink /data/omc/current → $TARGET_CSC..."
rm -f /data/omc/current
ln -s /data/omc/$TARGET_CSC /data/omc/current
echo "✅ Symlink creado"

# Verificar
echo ""
echo "🔍 Verificando estructura OMC:"
echo "   Directorio: $(ls -ld /data/omc/$TARGET_CSC | awk '{print $1, $3, $4}')"
echo "   Symlink: $(readlink /data/omc/current)"
echo "   Contenido:"
ls -la /data/omc/$TARGET_CSC/ | head -10

# Establecer permisos
echo ""
echo "🔸 Estableciendo permisos..."
chown -R system:system /data/omc/$TARGET_CSC
chmod -R 755 /data/omc/$TARGET_CSC
echo "✅ Permisos establecidos"

# Actualizar propiedades OMC
echo ""
echo "🔸 Actualizando propiedades OMC..."
setprop persist.sys.omc_path "/data/omc/$TARGET_CSC"
setprop persist.sys.omc_root "/system/csc/$TARGET_CSC"
setprop persist.sys.omcnw_path "/data/omc/$TARGET_CSC"
echo "✅ Propiedades OMC actualizadas"

echo ""
echo "═══════════════════════════════════════════════════"
echo " ✅ OMC CONFIGURADO"
echo "═══════════════════════════════════════════════════"
```

### PASO 8: Reiniciar Servicios

```bash
#!/system/bin/sh
# 8_reiniciar_servicios.sh - Ejecutar como root

TARGET_CSC="OWO"

echo "═══════════════════════════════════════════════════"
echo " PASO 8: REINICIAR SERVICIOS"
echo "═══════════════════════════════════════════════════"

# Función para iniciar servicio
start_service() {
    local service=$1
    echo "🔸 Iniciando $service..."
    start "$service" 2>/dev/null && echo "   ✅ $service iniciado" || echo "   ⚠️  $service no se pudo iniciar"
    sleep 1
}

echo ""
echo "📱 Reiniciando servicios vendor..."
start_service vendor.samsung.hardware.radio-service
start_service vendor.samsung.hardware.sehradio-service

echo ""
echo "📱 Reiniciando servicios RIL..."
start_service secril_config_svc
sleep 2
start_service rild
sleep 2

echo ""
echo "📱 Iniciando aplicaciones telephony..."
echo "🔸 Iniciando Phone app..."
am start -n com.android.phone/.PhoneApp 2>/dev/null && echo "   ✅ Phone iniciado" || echo "   ℹ️  Phone no se pudo iniciar"

echo ""
echo "📱 Enviando broadcasts de activación..."
am broadcast -a android.intent.action.SIM_STATE_CHANGED 2>/dev/null && echo "   ✅ SIM_STATE_CHANGED enviado"
am broadcast -a com.samsung.intent.action.CSC_UPDATE_TEST 2>/dev/null && echo "   ✅ CSC_UPDATE_TEST enviado"
am broadcast -a com.samsung.intent.action.CSC_COMPARE 2>/dev/null && echo "   ✅ CSC_COMPARE enviado"
am broadcast -a com.samsung.intent.action.CSC_CHAMELEON 2>/dev/null && echo "   ✅ CSC_CHAMELEON enviado"

echo ""
echo "⏳ Esperando 5 segundos para estabilización..."
sleep 5

echo ""
echo "🔍 Verificando servicios activos:"
ps -A | grep -E "rild|secril|phone" || echo "⚠️  Algunos servicios pueden no estar corriendo"

echo ""
echo "═══════════════════════════════════════════════════"
echo " ✅ SERVICIOS REINICIADOS"
echo "═══════════════════════════════════════════════════"
```

### PASO 9: Verificación Final

```bash
#!/system/bin/sh
# 9_verificacion_final.sh - Ejecutar como root

TARGET_CSC="OWO"

echo "═══════════════════════════════════════════════════"
echo " PASO 9: VERIFICACIÓN FINAL"
echo "═══════════════════════════════════════════════════"

PASS=0
FAIL=0

# Función de verificación
check() {
    local desc=$1
    local expected=$2
    local actual=$3
    
    if [ "$actual" = "$expected" ]; then
        echo "   ✅ $desc: $actual"
        PASS=$((PASS+1))
        return 0
    else
        echo "   ❌ $desc: $actual (esperado: $expected)"
        FAIL=$((FAIL+1))
        return 1
    fi
}

echo ""
echo "【 1. ARCHIVOS EFS 】"
if [ "$(id -u)" -eq 0 ]; then
    check "mps_code.dat" "$TARGET_CSC" "$(cat /efs/imei/mps_code.dat 2>/dev/null || echo 'ERROR')"
    check "sales_code.dat" "$TARGET_CSC" "$(cat /efs/imei/sales_code.dat 2>/dev/null || echo 'ERROR')"
else
    echo "   ⚠️  Se requiere root para verificar EFS"
fi

echo ""
echo "【 2. VENDOR EFS 】"
if [ -f /mnt/vendor/efs/telephony.prop ]; then
    echo "   telephony.prop:"
    grep -E "sales_code|sec_cid" /mnt/vendor/efs/telephony.prop | while read line; do
        echo "      $line"
    done
else
    echo "   ℹ️  telephony.prop no existe"
fi

echo ""
echo "【 3. PROPIEDADES PERSIST 】"
check "persist.sys.sec_cid" "$TARGET_CSC" "$(getprop persist.sys.sec_cid)"
check "persist.sys.sec_pcid" "$TARGET_CSC" "$(getprop persist.sys.sec_pcid)"
check "persist.ril.matched_code" "$TARGET_CSC" "$(getprop persist.ril.matched_code)"

echo ""
echo "【 4. PROPIEDADES OMC 】"
omc_path=$(getprop persist.sys.omc_path)
if echo "$omc_path" | grep -q "$TARGET_CSC"; then
    echo "   ✅ persist.sys.omc_path: $omc_path"
    PASS=$((PASS+1))
else
    echo "   ❌ persist.sys.omc_path: $omc_path (debe contener $TARGET_CSC)"
    FAIL=$((FAIL+1))
fi

echo ""
echo "【 5. PROPIEDADES RIL 】"
ril_sales=$(getprop ril.sales_code)
echo "   ril.sales_code: $ril_sales $([ "$ril_sales" = "$TARGET_CSC" ] && echo '✅' || echo '⚠️ (temporal, se actualizará al reiniciar)')"

echo ""
echo "【 6. BUILD.PROP 】"
if grep -q "ro.csc.sales_code=$TARGET_CSC" /system/build.prop 2>/dev/null; then
    echo "   ✅ /system/build.prop contiene ro.csc.sales_code=$TARGET_CSC"
    PASS=$((PASS+1))
else
    echo "   ❌ /system/build.prop NO contiene ro.csc.sales_code=$TARGET_CSC"
    FAIL=$((FAIL+1))
fi

echo ""
echo "【 7. ESTRUCTURA OMC 】"
if [ -d /data/omc/$TARGET_CSC ]; then
    echo "   ✅ /data/omc/$TARGET_CSC existe"
    PASS=$((PASS+1))
else
    echo "   ❌ /data/omc/$TARGET_CSC NO existe"
    FAIL=$((FAIL+1))
fi

if [ -L /data/omc/current ]; then
    symlink_target=$(readlink /data/omc/current)
    if echo "$symlink_target" | grep -q "$TARGET_CSC"; then
        echo "   ✅ Symlink correcto: $symlink_target"
        PASS=$((PASS+1))
    else
        echo "   ❌ Symlink incorrecto: $symlink_target"
        FAIL=$((FAIL+1))
    fi
else
    echo "   ❌ Symlink /data/omc/current NO existe"
    FAIL=$((FAIL+1))
fi

echo ""
echo "【 8. SERVICIOS 】"
if pgrep -f rild > /dev/null; then
    echo "   ✅ rild está corriendo"
    PASS=$((PASS+1))
else
    echo "   ❌ rild NO está corriendo"
    FAIL=$((FAIL+1))
fi

if pgrep -f secril_config_svc > /dev/null; then
    echo "   ✅ secril_config_svc está corriendo"
    PASS=$((PASS+1))
else
    echo "   ❌ secril_config_svc NO está corriendo"
    FAIL=$((FAIL+1))
fi

# Resumen
echo ""
echo "═══════════════════════════════════════════════════"
echo " RESULTADO FINAL"
echo "═══════════════════════════════════════════════════"
echo ""
echo "✅ Verificaciones exitosas: $PASS"
echo "❌ Verificaciones fallidas: $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "🎉 ¡TODAS LAS VERIFICACIONES PASARON!"
    echo ""
    echo "🔄 SIGUIENTE PASO:"
    echo "   1. Reiniciar el dispositivo: reboot"
    echo "   2. Después del reinicio, verificar:"
    echo "      getprop ro.csc.sales_code"
    echo "   3. Debe mostrar: $TARGET_CSC"
else
    echo "⚠️  ALGUNAS VERIFICACIONES FALLARON"
    echo ""
    echo "🔧 ACCIONES RECOMENDADAS:"
    echo "   1. Revisar los pasos que fallaron"
    echo "   2. Re-ejecutar los scripts correspondientes"
    echo "   3. Si persiste, reiniciar y verificar"
fi

echo ""
echo "═══════════════════════════════════════════════════"
```

### PASO 10: Script Master - Ejecuta Todo

```bash
#!/system/bin/sh
# MASTER_cambio_csc_completo.sh
# Ejecuta TODOS los pasos automáticamente

echo "╔═══════════════════════════════════════════════════╗"
echo "║  CAMBIO COMPLETO DE CSC: TPA → OWO                ║"
echo "║  Script Master - Ejecución Automática            ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# Verificar root
if [ "$(id -u)" -ne 0 ]; then
    echo "❌ ERROR: Se requiere ROOT"
    echo "Ejecuta: su -c 'sh MASTER_cambio_csc_completo.sh'"
    exit 1
fi

# Directorio de scripts
SCRIPT_DIR="/sdcard/csc_scripts"

if [ ! -d "$SCRIPT_DIR" ]; then
    echo "❌ ERROR: Directorio de scripts no encontrado: $SCRIPT_DIR"
    echo "Asegúrate de que todos los scripts estén en $SCRIPT_DIR"
    exit 1
fi

cd "$SCRIPT_DIR"

# Lista de scripts
SCRIPTS=(
    "0_preparacion.sh"
    "1_detener_servicios.sh"
    "2_modificar_efs.sh"
    "3_modificar_vendor_efs.sh"
    "4_modificar_buildprop.sh"
    "5_establecer_propiedades.sh"
    "6_limpiar_caches.sh"
    "7_configurar_omc.sh"
    "8_reiniciar_servicios.sh"
    "9_verificacion_final.sh"
)

# Ejecutar cada script
for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        echo ""
        echo "▶️  Ejecutando: $script"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        sh "$script"
        
        if [ $? -ne 0 ]; then
            echo ""
            echo "❌ ERROR en $script"
            echo "¿Continuar de todos modos? (s/n)"
            read -r respuesta
            if [ "$respuesta" != "s" ]; then
                echo "Ejecución abortada"
                exit 1
            fi
        fi
    else
        echo "⚠️  Script no encontrado: $script"
    fi
done

echo ""
echo "╔═══════════════════════════════════════════════════╗"
echo "║  ✅ TODOS LOS PASOS COMPLETADOS                   ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""
echo "🔄 REINICIAR AHORA"
echo ""
echo "   reboot"
echo ""
```

---

## 📋 RESUMEN Y PRÓXIMOS PASOS

### Archivos Modificados

| Ubicación | Archivo | Cambio |
|-----------|---------|--------|
| `/efs/imei/` | `mps_code.dat` | TPA → OWO |
| `/efs/imei/` | `sales_code.dat` | TPA → OWO |
| `/mnt/vendor/efs/` | `telephony.prop` | Múltiples propiedades → OWO |
| `/system/` | `build.prop` | ro.csc.sales_code → OWO |
| `/vendor/` | `build.prop` | ro.csc.sales_code → OWO |
| Runtime | Propiedades persist.* | Todas → OWO |
| `/data/omc/` | Estructura completa | TPA → OWO |

### Comandos Rápidos de Verificación

```bash
# Estado CSC después del reinicio
getprop ro.csc.sales_code          # Debe ser: OWO
getprop ril.sales_code             # Debe ser: OWO
cat /efs/imei/mps_code.dat         # Debe ser: OWO

# Formato completo esperado
getprop ro.build.display.id
# Debe contener: SAOMC_SM-S916B_OWO_OWO_16_0009
```

### Si el Cambio No Funciona

1. **Factory Reset** (borra datos)
```bash
# Desde recovery
# Wipe data/factory reset
```

2. **Restaurar Backup**
```bash
dd if=/sdcard/CSC_FULL_BACKUP_*/efs_FULL.img of=/dev/block/by-name/efs
```

3. **Flash CSC OWO via Odin**
- Descargar firmware OWO completo
- Flashear solo el archivo CSC con Odin

---

**Versión:** 3.0 Final  
**Fecha:** 2024-12-28  
**Tipo:** Guía Paso a Paso Completa  
**CSC:** TPA → OWO (Completo: OWO/OWO,OWO/OWO)
