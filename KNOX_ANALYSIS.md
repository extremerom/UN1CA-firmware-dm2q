# 🔐 Análisis de Samsung Knox - Ingeniería Inversa y Bypass

## 📋 Información General de Knox

Samsung Knox es una plataforma de seguridad de nivel empresarial integrada en dispositivos Samsung Galaxy.

### Componentes Principales de Knox

```
Knox Platform
├── TrustZone (ARM Trusted Execution Environment)
├── TIMA (TrustZone-based Integrity Measurement Architecture)
├── RKP (Real-time Kernel Protection)
├── Secure Boot
├── DM-Verity
├── Knox Container
└── Knox Workspace
```

---

## 🔍 Aplicaciones Knox Identificadas en el Firmware

### Aplicaciones Knox en `/system/priv-app/`

```bash
# Buscar apps Knox en el firmware
find system/system/priv-app -name "*knox*" -o -name "*Knox*" -o -name "*KNOX*"
find system/system/priv-app -name "*secure*" -o -name "*Secure*"
find system/system/priv-app -name "*container*" -o -name "*Container*"
```

### Apps Knox Comunes en Samsung

1. **KnoxCore** - Core de Knox
2. **KnoxAttestationAgent** - Verificación de integridad
3. **KnoxAnalyticsUploader** - Telemetría Knox
4. **KnoxContainerAgent** - Gestor de contenedor
5. **KnoxVpnPacProcessor** - VPN Knox
6. **KnoxGuard** - Anti-robo Knox
7. **SecureFolder** - Carpeta segura
8. **SamsungDeviceHealthManager** - Salud del dispositivo

---

## 🔬 Análisis de Componentes Knox

### 1. Knox Bootloader y Verificación

**Ubicación**: `/dev/block/by-name/boot`

```bash
# Verificar estado de Knox
getprop ro.boot.warranty_bit
# 0 = Knox intacto
# 1 = Knox tripped (garantía invalidada)

getprop ro.boot.verifiedbootstate
# green = Verified boot OK
# yellow = Bootloader unlocked
# orange = Custom OS
# red = Failed verification

getprop ro.boot.vbmeta.device_state
# locked = Secure
# unlocked = Insecure
```

### 2. Knox TrustZone

**Componente**: Procesador seguro ARM

```
TrustZone Architecture:
┌─────────────────────────────┐
│    Normal World (Android)   │
│  - Apps                     │
│  - System services          │
│  - Kernel                   │
└─────────────┬───────────────┘
              │ SMC (Secure Monitor Call)
              │
┌─────────────▼───────────────┐
│    Secure World (Knox)      │
│  - Knox services            │
│  - Crypto operations        │
│  - Key storage              │
│  - Attestation              │
└─────────────────────────────┘
```

**Bibliotecas relacionadas**:
```bash
# Buscar librerías TrustZone
find vendor/lib64 -name "*tz*" -o -name "*tee*"
# Ej: libGPTEE_system.so, libGPreqcancel_svc.so
```

### 3. Knox TIMA (Integrity Measurement)

**Función**: Mide y verifica la integridad del sistema en tiempo de ejecución.

```bash
# Verificar logs TIMA
logcat -s TIMA:V

# Propiedades TIMA
getprop ro.config.tima
getprop security.ASKS.policy_version
```

**Componentes TIMA**:
- **Periodic Kernel Measurement (PKM)**
- **Defex (DEFense EXtension)**
- **LKMAUTH (Loadable Kernel Module Authentication)**

### 4. Knox RKP (Real-time Kernel Protection)

**Función**: Protege el kernel contra modificaciones en tiempo real.

```bash
# Verificar RKP
dmesg | grep -i rkp
dmesg | grep -i "uh "  # Hypervisor

# RKP opera a nivel de hypervisor (EL2)
# Protege:
# - Tablas de páginas del kernel
# - Código del kernel
# - Datos críticos
```

### 5. Knox DM-Verity

**Función**: Verificación de integridad de particiones del sistema.

```bash
# Verificar DM-Verity
getprop ro.boot.veritymode
# enforcing = Activo
# disabled = Desactivado

# Ver particiones verificadas
cat /proc/mounts | grep dm-
```

---

## 🛠️ Ingeniería Inversa de Apps Knox

### Método 1: Extraer y Decompila Apps Knox

```bash
# Buscar APKs Knox
find system/system/priv-app -name "*nox*" -name "*.apk"

# Ejemplo: KnoxAnalyticsUploader
cd /home/runner/work/UN1CA-firmware-dm2q/UN1CA-firmware-dm2q
mkdir -p knox_analysis

# Decompilacion con jadx
/tmp/jadx/bin/jadx -d knox_analysis/KnoxAnalytics \
  system/system/priv-app/SamsungAnalytics/SamsungAnalytics.apk
```

### Método 2: Analizar Librerías Nativas Knox

```bash
# Buscar librerías Knox
find vendor/lib64 -name "*knox*" -o -name "*skg*"

# Ejemplo: libskg.so (Samsung Knox Guard)
strings vendor/lib64/libskg.so | grep -i "knox\|guard"

# Análisis con Ghidra o IDA Pro
# (requiere herramientas de RE avanzadas)
```

### Método 3: Interceptar Comunicación Knox

```bash
# Logs de Knox
logcat -s KnoxCore:V KnoxAttestationAgent:V

# Interceptar con Frida
frida -U -f com.samsung.android.knox.analytics -l knox_hook.js
```

**Script Frida para Knox** (`knox_hook.js`):
```javascript
Java.perform(function() {
    // Hook KnoxAnalyticsUploader
    var KnoxAnalytics = Java.use("com.samsung.android.knox.analytics.Uploader");
    
    KnoxAnalytics.uploadData.implementation = function(data) {
        console.log("[Knox] Uploading data: " + data);
        return this.uploadData(data);
    };
    
    // Hook attestation
    var Attestation = Java.use("com.samsung.android.knox.attestation.SemRemoteAttestation");
    
    Attestation.startAttestation.implementation = function() {
        console.log("[Knox] Attestation started");
        return this.startAttestation();
    };
});
```

---

## 🔓 Bypass de Knox (Propósitos Educativos)

### ⚠️ ADVERTENCIA LEGAL

**NO RECOMENDADO**: Bypass de Knox puede:
- Invalidar garantía permanentemente
- Bloquear Samsung Pay/Knox Secure Folder
- Causar brick del dispositivo
- Violar términos de servicio

### Método 1: Desactivar Knox Counter (Pre-Root)

**Imposible después de trip**. El contador Knox es irreversible.

```bash
# Verificar antes de rootear
getprop ro.boot.warranty_bit
# Si es 0, Knox está intacto
# Si es 1, ya está tripped (irreversible)
```

### Método 2: Ocultar Root de Knox (Post-Root)

```bash
# Con Magisk instalado:

# 1. Magisk Hide (deprecated en v24+)
magisk --hide com.samsung.android.knox.attestation

# 2. Zygisk DenyList (Magisk v24+)
# Settings → Zygisk → Enforce DenyList
# Add: All Knox apps

# 3. Módulos Magisk recomendados:
# - Universal SafetyNet Fix
# - Shamiko
# - Knox Patcher
```

### Método 3: Desactivar Servicios Knox

```bash
# Desactivar apps Knox (requiere root)
pm disable com.samsung.android.knox.analytics.uploader
pm disable com.samsung.android.knox.attestation
pm disable com.samsung.android.knox.containeragent
pm disable com.sec.enterprise.knox.cloudmdm.smdms
pm disable com.samsung.android.knox.kpu

# Verificar
pm list packages -d | grep knox
```

### Método 4: Parchear Knox en ROM Custom

```bash
# En ROM custom (LineageOS, etc.):

# 1. Remover apps Knox del sistema
rm -rf /system/priv-app/*knox*
rm -rf /system/priv-app/*Knox*

# 2. Remover librerías Knox
rm -rf /vendor/lib64/*knox*
rm -rf /vendor/lib64/libskg*

# 3. Modificar build.prop
# Cambiar: ro.config.knox = 0
```

### Método 5: SELinux Permissive (Temporal)

```bash
# Cambiar a permissive (desactiva algunas protecciones Knox)
setenforce 0

# Verificar
getenforce
# Permissive = Knox parcialmente desactivado
# Enforcing = Knox activo

# NOTA: Se resetea al reiniciar
```

---

## 🔍 Análisis de Apps Knox Específicas

### Knox Analytics Uploader

**Paquete**: `com.samsung.android.knox.analytics`

**Funciones**:
- Recopila métricas de uso
- Telemetría de seguridad
- Reporta intentos de bypass

**Decompilación**:
```bash
jadx -d knox_analysis/Analytics \
  system/system/priv-app/SamsungAnalytics/SamsungAnalytics.apk

# Buscar endpoints
grep -r "https://" knox_analysis/Analytics/sources/
```

**Endpoints identificados** (ejemplo):
```
https://analytics.samsungknox.com/v1/upload
https://kcs.samsungknox.com/attestation
```

### Knox Attestation Agent

**Paquete**: `com.samsung.android.knox.attestation`

**Funciones**:
- Verifica integridad del dispositivo
- Attestation remoto
- Generación de certificados de confianza

**Clases clave**:
```java
com.samsung.android.knox.attestation.SemRemoteAttestation
com.samsung.android.knox.attestation.AttestationPolicy
```

### Knox Container Agent

**Paquete**: `com.samsung.android.knox.containeragent`

**Funciones**:
- Gestión de Knox Workspace
- Aislamiento de apps corporativas
- Políticas MDM

**Análisis de permisos**:
```xml
<uses-permission android:name="com.samsung.android.knox.permission.KNOX_CONTAINER" />
<uses-permission android:name="com.samsung.android.knox.permission.KNOX_CONTAINER_VPN" />
```

---

## 🛡️ Protecciones Knox Contra Ingeniería Inversa

### 1. Code Obfuscation

Knox usa ProGuard/R8 agresivo:
```java
// Original
public class KnoxAttestationService

// Ofuscado
public class a.b.c.d
```

### 2. Native Code

Funciones críticas en C/C++:
```bash
# Librerías nativas Knox
libskg.so          # Samsung Knox Guard
libknox_cert.so    # Certificados Knox
libknoxcustom.so   # Knox Customization
```

### 3. String Encryption

Strings sensibles encriptados:
```java
// No encontrarás strings en claro como:
// "https://knox.samsung.com"
// Están encriptados y se desencriptan en runtime
```

### 4. Anti-Debugging

```java
// Detección de debugging
if (Debug.isDebuggerConnected()) {
    System.exit(0);
}

// Detección de Frida/Xposed
if (checkFramework()) {
    terminateApp();
}
```

---

## 🔬 Herramientas para Análisis de Knox

### Análisis Estático

```bash
# jadx - Decompilador DEX a Java
jadx -d output app.apk

# Ghidra - Análisis de binarios nativos
ghidra

# APKTool - Decompilación a Smali
apktool d app.apk

# grep/strings - Búsqueda de strings
strings libskg.so | grep knox
```

### Análisis Dinámico

```bash
# Frida - Hooking runtime
frida -U -f com.package.name -l script.js

# strace - System call tracing
strace -p PID

# logcat - Android logging
logcat -s KnoxCore:V

# tcpdump - Network analysis
tcpdump -i any -w knox_traffic.pcap
```

### Herramientas Especializadas

1. **QARK** - Quick Android Review Kit
2. **MobSF** - Mobile Security Framework
3. **Objection** - Runtime Mobile Exploration
4. **r2frida** - Radare2 + Frida

---

## 📊 Comparación: Knox vs Root

| Aspecto | Con Knox | Sin Knox (Rooted/Custom ROM) |
|---------|----------|-------------------------------|
| Seguridad | ✅ Muy alta | ⚠️ Reducida |
| Samsung Pay | ✅ Funciona | ❌ No funciona |
| Secure Folder | ✅ Funciona | ❌ No funciona |
| Garantía | ✅ Válida | ❌ Invalidada |
| Flexibilidad | ⚠️ Limitada | ✅ Total |
| Comandos AT | ⚠️ Bloqueados | ✅ Accesibles |
| Socket RIL | ⚠️ Restringido | ✅ Disponible |

---

## 🎯 Casos de Uso: Cuándo Bypass Knox

### Bypass Recomendado Si:

- ✅ Necesitas acceso completo al sistema
- ✅ Desarrollo/investigación avanzada
- ✅ No usas Samsung Pay/Secure Folder
- ✅ Garantía ya expirada/no importante
- ✅ Dispositivo de pruebas/desarrollo

### Mantener Knox Si:

- ✅ Usas Samsung Pay regularmente
- ✅ Necesitas Secure Folder corporativo
- ✅ Garantía es importante
- ✅ Dispositivo principal
- ✅ Políticas MDM empresariales

---

## 🔐 Knox en Firmware UN1CA

### Apps Knox Identificadas en el Dump

```bash
# Buscar en el firmware extraído
cd /home/runner/work/UN1CA-firmware-dm2q/UN1CA-firmware-dm2q

# Apps relacionadas con seguridad
find system/system/priv-app -name "*Secure*"
find system/system/priv-app -name "*Guard*"
find system/system/priv-app -name "*Health*"

# Ejemplos encontrados:
# - SamsungDeviceHealthManagerService
# - vaultkeeperd (binary)
# - ssgtzd (Samsung Security GTZ daemon)
```

### Servicios Knox Activos

Según tu `ls /dev/socket/`:
```
vaultkeeper/       # Knox Vault Keeper
ssgtzd             # Samsung Security daemon
```

Estos servicios son parte de Knox y están activos en tu dispositivo.

---

## 🛠️ Script de Análisis de Knox

```bash
#!/system/bin/sh
# knox_analysis.sh

echo "=== Knox Status Analysis ==="

echo "1. Knox Counter:"
getprop ro.boot.warranty_bit

echo ""
echo "2. Verified Boot State:"
getprop ro.boot.verifiedbootstate

echo ""
echo "3. VBMeta Device State:"
getprop ro.boot.vbmeta.device_state

echo ""
echo "4. SELinux Status:"
getenforce

echo ""
echo "5. Knox Apps Enabled:"
pm list packages | grep -i knox | wc -l

echo ""
echo "6. Knox Services:"
ps -A | grep -iE "knox|ssg|vault"

echo ""
echo "7. Knox Sockets:"
ls -la /dev/socket/ | grep -iE "knox|vault|ssg"

echo ""
echo "8. DM-Verity Status:"
getprop ro.boot.veritymode

echo ""
echo "9. Knox Logs (last 20):"
logcat -d -s KNOX:V | tail -20
```

---

## 📚 Referencias y Recursos

### Documentación Oficial

- Samsung Knox Documentation: https://docs.samsungknox.com/
- Knox SDK: https://seap.samsung.com/sdk/knox-sdk
- Knox Warranty: https://www.samsungknox.com/en/knox-warranty

### Herramientas

- ODIN: Flash firmware oficial
- Heimdall: Alternativa open-source a ODIN
- Magisk: Root con Knox bypass parcial

### Comunidades

- XDA Developers Forums
- Android Modding Communities
- Security Research Groups

---

## ⚠️ Disclaimer Legal

Este documento es **SOLO PARA FINES EDUCATIVOS**.

**NO me hago responsable de**:
- Pérdida de garantía
- Brick del dispositivo
- Pérdida de datos
- Problemas legales
- Violación de términos de servicio

**Bypass de Knox puede**:
- Trip del contador Knox (irreversible)
- Invalidar garantía permanentemente
- Bloquear Samsung Pay/Knox
- Causar problemas de estabilidad

---

**Análisis creado**: Diciembre 2024  
**Firmware**: UN1CA (SM-S916B / dm2q)  
**Knox Version**: (verificar con: getprop ro.config.knox)  
**Propósito**: Educativo e investigación

Para más información sobre comandos AT y acceso al modem sin Knox:
- Ver: TROUBLESHOOTING_RIL_SOCKET.md
- Ver: AT_COMMANDS_EXECUTION_GUIDE.md
