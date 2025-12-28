# Guía Avanzada de Modificación Manual de CSC con Root
## Análisis Profundo de Telephony, CIDManager y Frameworks

---

## 📋 Tabla de Contenidos
1. [Análisis Detallado de Componentes](#análisis-detallado-de-componentes)
2. [Estructura del Sistema CSC](#estructura-del-sistema-csc)
3. [Métodos de Modificación Manual](#métodos-de-modificación-manual)
4. [Explotación de Vulnerabilidades y Funciones](#explotación-de-vulnerabilidades-y-funciones)
5. [Comandos Shell para Modificación](#comandos-shell-para-modificación)
6. [Análisis del Dump](#análisis-del-dump)

---

## 🔬 Análisis Detallado de Componentes

### 1. CIDManager.apk - El Controlador Central del CSC

**Ubicación**: `/system/priv-app/CIDManager/CIDManager.apk`

**Función Principal**: CIDManager (Carrier ID Manager) es el componente más crítico para el cambio de CSC. Gestiona la identificación del operador, la activación basada en SIM y la configuración dinámica del CSC.

#### Clases Clave Identificadas:

##### 1.1. `i/a.smali` - Gestor de Sales Code
```smali
# Propiedades que lee:
const-string v0, "ro.csc.sales_code"
const-string p2, "ro.csc.countryiso_code"
const-string p1, "ro.csc.country_code"
```

**Funcionalidad**: Esta clase obtiene el sales code actual y lo valida contra la lista de códigos unificados.

##### 1.2. `c/a.smali` - Sistema de Propiedades
```smali
# Propiedades críticas del sistema:
persist.sys.sec_cid          # CID actual
persist.sys.sec_pcid         # PCID (Pre-loaded CID)
persist.sys.matched_code     # Código matched del operador
persist.sys.omc_path         # Ruta de OMC (Open Market Customization)
persist.sys.omc_root         # Raíz de OMC
persist.sys.singlesku_activate  # Activación de SKU único
```

**Descubrimiento Importante**: CIDManager usa propiedades `persist.*` que sobreviven a reinicios y no son de solo lectura como `ro.*`.

##### 1.3. `s/c.smali` - SIMBasedChangeCSC
```smali
const-string v1, "[SIMBasedChangeCSC] SIMBasedActivation ("
```

**Funcionalidad**: Esta clase maneja el cambio automático de CSC basado en la tarjeta SIM insertada. Es el mecanismo que Samsung usa para Multi-CSC.

**Punto de Explotación**: Si podemos engañar a esta clase sobre qué SIM está insertada, podemos activar cualquier CSC sin cambiar el EFS físicamente.

##### 1.4. `DeletePackages/b.smali` - Acceso a EFS
```smali
const-string v8, "sales_code.dat"
# Verifica: /efs/imei/sales_code.dat
```

**Funcionalidad**: Esta clase accede directamente al archivo `sales_code.dat` en EFS para leer/escribir el CSC.

#### Permisos de CIDManager:
```xml
<uses-permission android:name="android.permission.DELETE_PACKAGES"/>
<uses-permission android:name="android.permission.CLEAR_APP_USER_DATA"/>
<uses-permission android:name="com.samsung.permission.SHOW_MASTER_CLEAR_SETTINGS"/>
```

**Implicaciones de Seguridad**: CIDManager tiene permisos de sistema completo, incluyendo borrar paquetes y datos de usuario.

#### Broadcasts que CIDManager Recibe:
```xml
<action android:name="android.intent.action.SIM_STATE_CHANGED"/>
<action android:name="com.samsung.intent.action.LAZY_BOOT_COMPLETE"/>
<action android:name="com.samsung.intent.action.OMCUPDATE_FINISH"/>
```

**Punto de Explotación**: Podemos enviar broadcasts falsos para activar el proceso de cambio de CSC.

---

### 2. TeleService.apk - Servicios de Telefonía

**Ubicación**: `/system/priv-app/TeleService/TeleService.apk`

**Tamaño DEX**: 5.0 MB (classes.dex)

**Función Principal**: Gestiona todos los servicios de telefonía, incluyendo llamadas, SMS, configuración de red y propiedades del RIL (Radio Interface Layer).

#### Strings CSC Encontradas:
```
ro.csc.countryiso_code
ro.csc.sales_code
```

**Descubrimiento**: TeleService lee propiedades CSC pero no las modifica. Es un consumidor, no un modificador.

---

### 3. SecTelephonyProvider.apk - Proveedor de Datos de Telefonía

**Ubicación**: `/system/priv-app/SecTelephonyProvider/SecTelephonyProvider.apk`

**Función Principal**: Content Provider que almacena y gestiona datos de telefonía, incluyendo APN, configuraciones de red, y sales code.

#### Propiedades Críticas Encontradas:
```
persist.sys.omc_path
persist.sys.omc_root
persist.sys.omc_support
persist.sys.sec_cid
persist.sys.sec_pcid
ro.csc.country_code
ro.csc.countryiso_code
ro.csc.sales_code
```

**Base de Datos**: Usa SQLite en `/data/data/com.android.providers.telephony/databases/`

**Punto de Explotación**: Podemos modificar directamente la base de datos para cambiar el sales_code almacenado.

---

### 4. telephony-common.jar - Framework de Telefonía

**Ubicación**: `/system/framework/telephony-common.jar`

**Función Principal**: Biblioteca base de Android para servicios de telefonía.

**Descubrimiento**: No contiene lógica específica de Samsung CSC. Samsung extiende esto con `telephony-ext.jar`.

---

### 5. CSC.apk - Aplicación de Gestión CSC

**Ubicación**: `/system/priv-app/CSC/CSC.apk`

Ya analizado anteriormente. Clases clave:
- CSC Ringtone Manager
- CSC Compare Service  
- CSC Update Service

---

## 🏗️ Estructura del Sistema CSC

### Niveles de Almacenamiento del CSC

```
┌─────────────────────────────────────────────────────┐
│ NIVEL 1: Propiedades de Solo Lectura (ro.*)        │
│ - ro.csc.sales_code                                 │
│ - ro.csc.country_code                               │
│ - ro.csc.countryiso_code                            │
│ Origen: /system/build.prop, /vendor/build.prop      │
│ Modificación: Requiere remount de /system           │
└─────────────────────────────────────────────────────┘
            ↓ Lee desde
┌─────────────────────────────────────────────────────┐
│ NIVEL 2: EFS Partition (Persistent Storage)        │
│ - /efs/imei/mps_code.dat                            │
│ - /efs/imei/sales_code.dat                          │
│ Modificación: Requiere root, afecta boot           │
└─────────────────────────────────────────────────────┘
            ↓ Sincroniza con
┌─────────────────────────────────────────────────────┐
│ NIVEL 3: Propiedades Persistentes (persist.*)      │
│ - persist.sys.sec_cid                               │
│ - persist.sys.sec_pcid                              │
│ - persist.sys.matched_code                          │
│ - persist.sys.omc_path                              │
│ Modificación: setprop (requiere root)              │
└─────────────────────────────────────────────────────┘
            ↓ Usa para configurar
┌─────────────────────────────────────────────────────┐
│ NIVEL 4: Propiedades de Runtime                    │
│ - ril.sales_code                                    │
│ - ril.official_cscver                               │
│ - ril.matchedcsc                                    │
│ Modificación: Temporal, se pierde al reiniciar     │
└─────────────────────────────────────────────────────┘
            ↓ Controla
┌─────────────────────────────────────────────────────┐
│ NIVEL 5: OMC (Open Market Customization)           │
│ - /data/omc/                                        │
│ - Archivos de configuración específicos del CSC    │
│ Modificación: Depende del CSC activo               │
└─────────────────────────────────────────────────────┘
```

### Flujo de Inicialización del CSC

```
Boot → init.rc ejecuta → 
    ↓
Lee /efs/imei/mps_code.dat →
    ↓
Establece ro.csc.sales_code →
    ↓
CIDManager.apk se inicia →
    ↓
Verifica SIM insertada →
    ↓
Compara con sales_code actual →
    ↓
¿Coincide? 
    ├─ SÍ → Continúa con CSC actual
    └─ NO → Inicia proceso de cambio de CSC
              ↓
         Copia archivos de /system/csc/[NUEVO_CSC]/
              ↓
         Actualiza /efs/imei/mps_code.dat
              ↓
         Actualiza persist.sys.*
              ↓
         Reinicia al finalizar
```

---

## 🔧 Métodos de Modificación Manual

### Método 1: Modificación Directa de EFS (Más Efectivo)

Este es el método más profundo y permanente.

#### Paso 1: Backup Crítico
```bash
#!/system/bin/sh
# Ejecutar como root

# Backup completo de EFS
dd if=/dev/block/by-name/efs of=/sdcard/efs_backup_$(date +%Y%m%d).img bs=4096

# Backup de archivos individuales
cp /efs/imei/mps_code.dat /sdcard/mps_code_backup.dat
cp /efs/imei/sales_code.dat /sdcard/sales_code_backup.dat

# Verificar backup
ls -lh /sdcard/*backup*
```

#### Paso 2: Montar EFS como RW
```bash
# Verificar punto de montaje actual
mount | grep efs

# Remontar como lectura-escritura
mount -o remount,rw /efs

# Verificar permisos
ls -la /efs/imei/
```

#### Paso 3: Modificar Sales Code
```bash
# Cambiar a OWO
echo "OWO" > /efs/imei/mps_code.dat
echo "OWO" > /efs/imei/sales_code.dat

# Establecer permisos correctos (CRÍTICO)
chown radio:radio /efs/imei/mps_code.dat
chown radio:radio /efs/imei/sales_code.dat
chmod 0644 /efs/imei/mps_code.dat
chmod 0644 /efs/imei/sales_code.dat

# Verificar cambios
cat /efs/imei/mps_code.dat
cat /efs/imei/sales_code.dat
ls -la /efs/imei/
```

#### Paso 4: Sincronizar y Proteger
```bash
# Sincronizar cambios al disco
sync

# Remontar como solo lectura
mount -o remount,ro /efs

# Verificar
mount | grep efs
```

---

### Método 2: Modificación de Propiedades del Sistema

Este método modifica las propiedades que CIDManager lee.

#### Paso 1: Identificar Propiedades Actuales
```bash
# Ver todas las propiedades CSC
getprop | grep -i csc
getprop | grep sales
getprop | grep persist.sys

# Propiedades específicas
getprop ro.csc.sales_code
getprop ril.sales_code
getprop persist.sys.sec_cid
```

#### Paso 2: Modificar Propiedades Persistentes
```bash
#!/system/bin/sh
# Ejecutar como root

# Establecer propiedades persistentes (sobreviven reboot)
setprop persist.sys.sec_cid OWO
setprop persist.sys.sec_pcid OWO
setprop persist.sys.matched_code OWO

# Establecer propiedades temporales
setprop ril.sales_code OWO
setprop ril.matchedcsc OWO

# Verificar
getprop | grep OWO
```

#### Paso 3: Modificar build.prop (Opcional pero Recomendado)
```bash
# Remontar /system como RW
mount -o remount,rw /system
mount -o remount,rw /vendor

# Backup de build.prop
cp /system/build.prop /sdcard/build.prop.backup
cp /vendor/build.prop /sdcard/vendor_build.prop.backup

# Modificar /system/build.prop
# Buscar y reemplazar o agregar:
sed -i 's/ro.csc.sales_code=.*/ro.csc.sales_code=OWO/' /system/build.prop

# Si no existe, agregar al final:
echo "ro.csc.sales_code=OWO" >> /system/build.prop
echo "persist.sys.sec_cid=OWO" >> /system/build.prop

# Remontar como RO
mount -o remount,ro /system
mount -o remount,ro /vendor
```

---

### Método 3: Explotación de CIDManager (Avanzado)

Este método explota el mecanismo de SIMBasedChangeCSC para activar el cambio.

#### Paso 1: Preparar Base de Datos de CIDManager
```bash
# Ubicación de la BD
cd /data/user_de/0/com.samsung.sec.android.application.csc/

# O alternativamente:
cd /data/data/com.samsung.sec.android.application.csc/

# Listar bases de datos
find . -name "*.db"

# Examinar con sqlite3 (si está disponible)
sqlite3 databases/carrier.db ".tables"
```

#### Paso 2: Limpiar Caché de CSC
```bash
# Detener CIDManager
am force-stop com.samsung.sec.android.application.csc

# Limpiar datos
rm -rf /data/data/com.samsung.sec.android.application.csc/cache/*
rm -rf /data/data/com.samsung.sec.android.application.csc/shared_prefs/*

# Limpiar caché de CSC global
rm -rf /data/csc/*
```

#### Paso 3: Enviar Broadcast de Activación
```bash
# Simular cambio de SIM para activar CIDManager
am broadcast -a android.intent.action.SIM_STATE_CHANGED

# Activar proceso de actualización de CSC
am broadcast -a com.samsung.intent.action.CSC_UPDATE_TEST

# Forzar comparación de CSC
am broadcast -a com.samsung.intent.action.CSC_COMPARE
```

#### Paso 4: Forzar Activación Manual
```bash
# Iniciar actividad de preconfig (código secreto)
am start -n com.samsung.sec.android.application.csc/.modules.preconfig.PreconfigActivity

# O usando intent directo
am start -a android.intent.action.MAIN -n com.samsung.sec.android.application.csc/.modules.preconfig.PreconfigActivity
```

---

### Método 4: Modificación de Base de Datos de Telephony Provider

#### Paso 1: Localizar Base de Datos
```bash
# Ubicación principal
cd /data/user_de/0/com.android.providers.telephony/databases/

# Listar bases de datos
ls -la *.db

# Base de datos principal: telephony.db
```

#### Paso 2: Examinar Estructura
```bash
# Usando sqlite3
sqlite3 telephony.db ".schema"

# Ver tablas
sqlite3 telephony.db ".tables"

# Buscar sales_code
sqlite3 telephony.db "SELECT * FROM carriers WHERE mcc='310';"
```

#### Paso 3: Modificar Entradas
```bash
# Backup primero
cp telephony.db /sdcard/telephony.db.backup

# Modificar (ejemplo - ajustar según estructura real)
sqlite3 telephony.db "UPDATE carriers SET numeric='310260' WHERE mcc='340';"

# Reiniciar proveedor
am force-stop com.android.providers.telephony
```

---

## 🐛 Explotación de Vulnerabilidades y Funciones

### Vulnerabilidad 1: Permisos de CIDManager

**Descripción**: CIDManager tiene permisos de sistema completo y puede ser activado mediante broadcasts.

**Explotación**:
```bash
# 1. Crear intent malicioso
am broadcast -a com.samsung.intent.action.CSC_CHAMELEON

# 2. Esto activa el modo "Chameleon" que cambia CSC dinámicamente

# 3. Verificar activación
logcat | grep CIDManager
```

### Vulnerabilidad 2: Race Condition en Boot

**Descripción**: Durante el boot, hay una ventana donde las propiedades no están protegidas.

**Explotación**:
```bash
# 1. Crear script en /data/local/userinit.sh (se ejecuta al boot)
cat > /data/local/userinit.sh << 'EOF'
#!/system/bin/sh
# Esperar a que el sistema esté listo
sleep 5

# Modificar propiedades antes de que CIDManager las lea
setprop persist.sys.sec_cid OWO
setprop ril.sales_code OWO

# Modificar EFS si es posible
mount -o remount,rw /efs
echo "OWO" > /efs/imei/mps_code.dat 2>/dev/null
mount -o remount,ro /efs
EOF

# 2. Dar permisos de ejecución
chmod 755 /data/local/userinit.sh

# 3. Reiniciar
reboot
```

### Vulnerabilidad 3: Symlink Attack en OMC

**Descripción**: El sistema OMC sigue enlaces simbólicos.

**Explotación**:
```bash
# 1. Crear estructura OMC falsa
mkdir -p /data/omc/OWO

# 2. Copiar estructura de CSC existente
cp -r /system/csc/TPA/* /data/omc/OWO/ 2>/dev/null || echo "Multi-CSC no disponible"

# 3. Crear symlink
rm -rf /data/omc/current
ln -s /data/omc/OWO /data/omc/current

# 4. Actualizar propiedad
setprop persist.sys.omc_path /data/omc/OWO
```

### Función Oculta: Service Mode CSC Change

**Descripción**: Samsung tiene modos de servicio ocultos.

**Acceso**:
```bash
# Método 1: Código secreto (marcar en teléfono)
# *#272*[IMEI]# 
# Donde [IMEI] son los últimos 4 dígitos de tu IMEI

# Método 2: Activity directa
am start -n com.samsung.sec.android.application.csc/.modules.preconfig.PreconfigActivity

# Método 3: ADB
adb shell am start -n com.sec.android.app.servicemodeapp/.ServiceModeApp
```

---

## 💻 Comandos Shell para Modificación Completa

### Script Completo de Modificación TPA → OWO

```bash
#!/system/bin/sh
# CSC_CHANGE_TPA_TO_OWO.sh
# Requiere ROOT
# Cambia CSC de TPA a OWO permanentemente

set -e

TARGET_CSC="OWO"
SOURCE_CSC="TPA"

echo "════════════════════════════════════════════"
echo "   Cambio de CSC: $SOURCE_CSC → $TARGET_CSC"
echo "════════════════════════════════════════════"
echo ""

# Verificar root
if [ "$(id -u)" -ne 0 ]; then
    echo "❌ ERROR: Se requiere ROOT"
    exit 1
fi

echo "✓ Root verificado"
echo ""

# ==========================================
# FASE 1: BACKUP
# ==========================================
echo "FASE 1: Realizando Backups..."
echo "──────────────────────────────────────────"

BACKUP_DIR="/sdcard/CSC_BACKUP_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup EFS
echo "→ Backing up EFS partition..."
dd if=/dev/block/by-name/efs of="$BACKUP_DIR/efs.img" bs=4096 2>/dev/null
echo "✓ EFS backed up"

# Backup archivos críticos
cp /efs/imei/mps_code.dat "$BACKUP_DIR/" 2>/dev/null || echo "! mps_code.dat no encontrado"
cp /efs/imei/sales_code.dat "$BACKUP_DIR/" 2>/dev/null || echo "! sales_code.dat no encontrado"
cp /system/build.prop "$BACKUP_DIR/system_build.prop" 2>/dev/null
cp /vendor/build.prop "$BACKUP_DIR/vendor_build.prop" 2>/dev/null

# Backup propiedades actuales
getprop > "$BACKUP_DIR/all_properties.txt"
getprop | grep -i csc > "$BACKUP_DIR/csc_properties.txt"

echo "✓ Backups completados en: $BACKUP_DIR"
echo ""

# ==========================================
# FASE 2: MODIFICACIÓN DE EFS
# ==========================================
echo "FASE 2: Modificando EFS..."
echo "──────────────────────────────────────────"

# Remontar EFS como RW
mount -o remount,rw /efs 2>/dev/null || echo "! No se pudo remontar /efs"

# Modificar sales code
echo "→ Modificando mps_code.dat..."
echo "$TARGET_CSC" > /efs/imei/mps_code.dat
chown radio:radio /efs/imei/mps_code.dat
chmod 0644 /efs/imei/mps_code.dat
echo "✓ mps_code.dat = $(cat /efs/imei/mps_code.dat)"

echo "→ Modificando sales_code.dat..."
echo "$TARGET_CSC" > /efs/imei/sales_code.dat
chown radio:radio /efs/imei/sales_code.dat
chmod 0644 /efs/imei/sales_code.dat
echo "✓ sales_code.dat = $(cat /efs/imei/sales_code.dat)"

# Sincronizar cambios
sync
sleep 1

# Remontar como RO
mount -o remount,ro /efs 2>/dev/null

echo "✓ EFS modificado correctamente"
echo ""

# ==========================================
# FASE 3: PROPIEDADES DEL SISTEMA
# ==========================================
echo "FASE 3: Modificando Propiedades del Sistema..."
echo "──────────────────────────────────────────"

# Propiedades persistentes
echo "→ Estableciendo propiedades persist.*..."
setprop persist.sys.sec_cid "$TARGET_CSC"
setprop persist.sys.sec_pcid "$TARGET_CSC"
setprop persist.sys.matched_code "$TARGET_CSC"
setprop persist.sys.omc_path "/system/csc/$TARGET_CSC"
echo "✓ Propiedades persist.* establecidas"

# Propiedades RIL temporales
echo "→ Estableciendo propiedades ril.*..."
setprop ril.sales_code "$TARGET_CSC"
setprop ril.matchedcsc "$TARGET_CSC"
echo "✓ Propiedades ril.* establecidas"

echo ""

# ==========================================
# FASE 4: MODIFICACIÓN DE BUILD.PROP
# ==========================================
echo "FASE 4: Modificando build.prop..."
echo "──────────────────────────────────────────"

# Remontar /system como RW
mount -o remount,rw / 2>/dev/null
mount -o remount,rw /system 2>/dev/null
mount -o remount,rw /vendor 2>/dev/null

# Modificar /system/build.prop
if [ -f /system/build.prop ]; then
    echo "→ Modificando /system/build.prop..."
    
    # Remover líneas antiguas de CSC si existen
    sed -i '/ro.csc.sales_code=/d' /system/build.prop
    sed -i '/persist.sys.sec_cid=/d' /system/build.prop
    
    # Agregar nuevas
    echo "" >> /system/build.prop
    echo "# CSC Modified to $TARGET_CSC" >> /system/build.prop
    echo "ro.csc.sales_code=$TARGET_CSC" >> /system/build.prop
    echo "persist.sys.sec_cid=$TARGET_CSC" >> /system/build.prop
    
    echo "✓ /system/build.prop modificado"
fi

# Sincronizar
sync
sleep 1

# Remontar como RO
mount -o remount,ro /system 2>/dev/null
mount -o remount,ro /vendor 2>/dev/null
mount -o remount,ro / 2>/dev/null

echo ""

# ==========================================
# FASE 5: LIMPIAR CACHÉS
# ==========================================
echo "FASE 5: Limpiando Cachés..."
echo "──────────────────────────────────────────"

# Detener servicios relacionados
echo "→ Deteniendo servicios..."
am force-stop com.samsung.sec.android.application.csc
am force-stop com.android.phone
am force-stop com.android.providers.telephony

# Limpiar cachés de CSC
echo "→ Limpiando cachés de CSC..."
rm -rf /data/csc/* 2>/dev/null
rm -rf /data/data/com.samsung.sec.android.application.csc/cache/* 2>/dev/null
rm -rf /data/data/com.samsung.sec.android.application.csc/shared_prefs/* 2>/dev/null

# Limpiar caché de sistema
rm -rf /cache/* 2>/dev/null

echo "✓ Cachés limpiados"
echo ""

# ==========================================
# FASE 6: ACTIVAR CAMBIO
# ==========================================
echo "FASE 6: Activando Cambio de CSC..."
echo "──────────────────────────────────────────"

# Enviar broadcasts de activación
echo "→ Enviando broadcasts de activación..."
am broadcast -a com.samsung.intent.action.CSC_UPDATE_TEST 2>/dev/null
am broadcast -a com.samsung.intent.action.CSC_COMPARE 2>/dev/null
am broadcast -a android.intent.action.SIM_STATE_CHANGED 2>/dev/null

echo "✓ Broadcasts enviados"
echo ""

# ==========================================
# FASE 7: VERIFICACIÓN
# ==========================================
echo "FASE 7: Verificando Cambios..."
echo "──────────────────────────────────────────"

echo "EFS:"
echo "  - mps_code.dat: $(cat /efs/imei/mps_code.dat 2>/dev/null || echo 'No legible')"
echo "  - sales_code.dat: $(cat /efs/imei/sales_code.dat 2>/dev/null || echo 'No legible')"
echo ""

echo "Propiedades Persist:"
echo "  - persist.sys.sec_cid: $(getprop persist.sys.sec_cid)"
echo "  - persist.sys.matched_code: $(getprop persist.sys.matched_code)"
echo ""

echo "Propiedades RIL:"
echo "  - ril.sales_code: $(getprop ril.sales_code)"
echo ""

# ==========================================
# FINALIZACIÓN
# ==========================================
echo "════════════════════════════════════════════"
echo "   ✓ Modificación Completada"
echo "════════════════════════════════════════════"
echo ""
echo "PASOS SIGUIENTES:"
echo "1. Reiniciar el dispositivo: reboot"
echo "2. Después del reinicio, verificar:"
echo "   getprop ro.csc.sales_code"
echo "3. Si CSC no cambió, realizar Factory Reset"
echo "   (ESTO BORRARÁ TODOS LOS DATOS!)"
echo ""
echo "BACKUP guardado en: $BACKUP_DIR"
echo "CRÍTICO: Copiar backup a PC antes de continuar!"
echo ""
echo "¿Reiniciar ahora? Ejecuta: reboot"
echo ""
```

---

## 📊 Análisis del Dump

### Herramienta de Análisis Completo

```bash
#!/system/bin/sh
# CSC_DUMP_ANALYZER.sh
# Analiza todo el estado del sistema relacionado con CSC

echo "════════════════════════════════════════════"
echo "   Análisis Completo de CSC"
echo "════════════════════════════════════════════"
echo ""

# Información del dispositivo
echo "【 INFORMACIÓN DEL DISPOSITIVO 】"
echo "──────────────────────────────────────────"
echo "Modelo: $(getprop ro.product.model)"
echo "Device: $(getprop ro.product.device)"
echo "Build: $(getprop ro.build.display.id)"
echo "Android: $(getprop ro.build.version.release)"
echo "Kernel: $(uname -r)"
echo ""

# CSC Actual
echo "【 CSC ACTUAL 】"
echo "──────────────────────────────────────────"
echo "ro.csc.sales_code: $(getprop ro.csc.sales_code)"
echo "ril.sales_code: $(getprop ril.sales_code)"
echo "persist.sys.sec_cid: $(getprop persist.sys.sec_cid)"
echo "persist.sys.sec_pcid: $(getprop persist.sys.sec_pcid)"
echo "persist.sys.matched_code: $(getprop persist.sys.matched_code)"
echo "ro.csc.country_code: $(getprop ro.csc.country_code)"
echo "ro.csc.countryiso_code: $(getprop ro.csc.countryiso_code)"
echo "ril.official_cscver: $(getprop ril.official_cscver)"
echo "ril.matchedcsc: $(getprop ril.matchedcsc)"
echo ""

# EFS
if [ "$(id -u)" -eq 0 ]; then
    echo "【 ARCHIVOS EFS (Root) 】"
    echo "──────────────────────────────────────────"
    if [ -f /efs/imei/mps_code.dat ]; then
        echo "mps_code.dat: $(cat /efs/imei/mps_code.dat)"
        ls -la /efs/imei/mps_code.dat
    else
        echo "mps_code.dat: NO ENCONTRADO"
    fi
    
    if [ -f /efs/imei/sales_code.dat ]; then
        echo "sales_code.dat: $(cat /efs/imei/sales_code.dat)"
        ls -la /efs/imei/sales_code.dat
    else
        echo "sales_code.dat: NO ENCONTRADO"
    fi
    
    echo ""
    echo "Partición EFS:"
    mount | grep efs
    echo ""
else
    echo "【 ARCHIVOS EFS 】"
    echo "──────────────────────────────────────────"
    echo "(Se requiere root para acceder a EFS)"
    echo ""
fi

# OMC
echo "【 OMC (Open Market Customization) 】"
echo "──────────────────────────────────────────"
echo "persist.sys.omc_path: $(getprop persist.sys.omc_path)"
echo "persist.sys.omc_root: $(getprop persist.sys.omc_root)"
echo "persist.sys.omc_support: $(getprop persist.sys.omc_support)"
echo "persist.sys.omcnw_path: $(getprop persist.sys.omcnw_path)"
echo ""

if [ -d /system/csc ]; then
    echo "Multi-CSC disponibles en /system/csc:"
    ls -1 /system/csc/ 2>/dev/null | head -10
else
    echo "Multi-CSC: NO DISPONIBLE"
fi
echo ""

# Red y SIM
echo "【 INFORMACIÓN DE RED Y SIM 】"
echo "──────────────────────────────────────────"
echo "Operador: $(getprop gsm.operator.alpha)"
echo "MCC/MNC: $(getprop gsm.operator.numeric)"
echo "País ISO: $(getprop gsm.operator.iso-country)"
echo "Estado SIM: $(getprop gsm.sim.state)"
echo "ICCID: $(getprop persist.radio.iccid)"
echo ""

# Aplicaciones CSC
echo "【 APLICACIONES CSC 】"
echo "──────────────────────────────────────────"
echo "CSC.apk:"
if [ -f /system/priv-app/CSC/CSC.apk ]; then
    ls -lh /system/priv-app/CSC/CSC.apk
    pm list packages | grep csc
else
    echo "  NO ENCONTRADO"
fi

echo ""
echo "CIDManager.apk:"
if [ -f /system/priv-app/CIDManager/CIDManager.apk ]; then
    ls -lh /system/priv-app/CIDManager/CIDManager.apk
    pm list packages | grep cidmanager
else
    echo "  NO ENCONTRADO"
fi
echo ""

# Build.prop
echo "【 BUILD.PROP CSC ENTRIES 】"
echo "──────────────────────────────────────────"
grep -i "csc\|sales" /system/build.prop 2>/dev/null | head -10 || echo "(No se encontraron entradas CSC en build.prop)"
echo ""

# Procesos activos
echo "【 PROCESOS RELACIONADOS CON CSC 】"
echo "──────────────────────────────────────────"
ps -A | grep -i "csc\|cidmanager\|phone" | head -10
echo ""

# Logs recientes
echo "【 LOGS RECIENTES DE CSC 】"
echo "──────────────────────────────────────────"
logcat -d | grep -i "CSC\|CIDManager\|sales_code" | tail -20
echo ""

echo "════════════════════════════════════════════"
echo "   Análisis Completo"
echo "════════════════════════════════════════════"
```

---

## 🔐 Notas de Seguridad Críticas

### ⚠️ ADVERTENCIAS IMPORTANTES

1. **SIEMPRE hacer backup de EFS antes de modificar**
   - La pérdida de EFS puede hacer que el dispositivo sea inutilizable
   - Guardar múltiples copias en ubicaciones seguras
   - Verificar integridad del backup antes de proceder

2. **Verificar compatibilidad de CSC**
   - No todos los CSC son compatibles con todos los modelos
   - OWO debe existir en la base de datos de Samsung para tu modelo
   - Verificar que las bandas de frecuencia sean compatibles

3. **Impacto en funciones del dispositivo**
   - VoLTE/VoWiFi pueden dejar de funcionar
   - Algunas apps del operador pueden no funcionar
   - Servicios de emergencia deben ser probados

4. **Knox y Warranty**
   - Modificar CSC puede disparar Knox
   - Garantía puede quedar invalidada
   - Samsung Pay y otras apps seguras pueden dejar de funcionar

### 🛡️ Medidas de Protección

1. **Antes de comenzar:**
   ```bash
   # Verificar que tienes acceso a recovery
   adb reboot recovery
   
   # Verificar que puedes flashear via Odin
   # Tener firmware stock descargado
   ```

2. **Durante el proceso:**
   ```bash
   # Mantener conexión ADB activa
   # No interrumpir el proceso
   # No apagar el dispositivo
   ```

3. **Plan de recuperación:**
   - Tener firmware stock completo
   - Tener Odin instalado
   - Conocer combinación de botones para modo Download
   - Tener backup de EFS disponible

---

## 📚 Referencias y Recursos

### Archivos Analizados
- `/system/priv-app/CIDManager/CIDManager.apk` (7658 clases smali)
- `/system/priv-app/TeleService/TeleService.apk` (5.0MB DEX)
- `/system/priv-app/SecTelephonyProvider/SecTelephonyProvider.apk`
- `/system/priv-app/CSC/CSC.apk`
- `/system/framework/telephony-common.jar`
- `/system/framework/telephony-ext.jar`

### Propiedades Clave Descubiertas
```
ro.csc.sales_code
ro.csc.country_code
ro.csc.countryiso_code
ril.sales_code
ril.official_cscver
ril.matchedcsc
persist.sys.sec_cid
persist.sys.sec_pcid
persist.sys.matched_code
persist.sys.omc_path
persist.sys.omc_root
persist.sys.singlesku_activate
```

### Broadcasts Importantes
```
com.samsung.intent.action.CSC_UPDATE_TEST
com.samsung.intent.action.CSC_COMPARE
com.samsung.intent.action.CSC_CHAMELEON
com.samsung.intent.action.OMCUPDATE_FINISH
android.intent.action.SIM_STATE_CHANGED
```

---

## 🎯 Conclusión

Esta guía proporciona un análisis profundo de cómo Samsung maneja el CSC en el firmware dm2q. Los métodos descritos permiten modificar el CSC de TPA a OWO de múltiples formas, desde modificación directa de EFS hasta explotación de funciones del sistema.

**Método Recomendado**: Combinación de Método 1 (EFS) + Método 2 (Propiedades) para máxima efectividad.

**Recuerda**: Siempre mantén backups y procede con precaución. El cambio de CSC es reversible si tienes los backups correctos.

---

**Versión**: 1.0  
**Fecha**: 2024-12-28  
**Dispositivo**: Samsung Galaxy S23+ (SM-S916B)  
**Firmware**: SAOMC_SM-S916B_OWO_TPA_16_0009
