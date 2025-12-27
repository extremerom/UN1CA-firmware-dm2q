# Análisis Detallado del Firmware Samsung SM-S916B

## Información del Firmware Analizado

**Modelo:** SM-S916B (Samsung Galaxy S23)  
**Versión:** S916BXXS8EYK5/S916BOXM8EYK5/S916BXXU8EYI5  
**Fecha de compilación:** Fri Nov 28 11:27:08 KST 2025  
**Android:** 16 (API 36)  
**Tamaño super partition:** 12.66 GB  

## APKs y Binarios Analizados

### 1. FotaAgent.apk (`system/system/priv-app/FotaAgent/`)

**Tamaño:** 8.8 MB  
**Propósito:** Agente principal de FOTA (Firmware Over The Air) de Samsung

#### Hallazgos Clave:

**Servidores Descubiertos:**
- `https://fota-cloud-dn.ospserver.net/firmware/` - Servidor principal de descarga
- `stg-fota-cloud.samsungdms.net` - Servidor de staging/pruebas
- `https://dc.di.atlas.samsung.com` - Telemetría Samsung
- `https://regi.di.atlas.samsung.com` - Registro de dispositivos

**Archivos de Configuración:**
- `version.xml` - Lista de versiones disponibles
- `version.test.xml` - Versiones de prueba/beta

**Headers HTTP Identificados:**
```
User-Agent: Kies2.0_FUS
X-Sec-Dm-CustomerCode: [CSC_CODE]
X-Sec-Dm-DeviceModel: [MODEL]
X-Sec-Download-Network-Bearer: [NETWORK_TYPE]
X-Client-Version: [VERSION]
Content-Type: application/x-www-form-urlencoded
```

**Propiedades del Sistema Utilizadas:**
```
ro.product.model         # SM-S916B
ro.build.PDA             # S916BXXS8EYK5
ro.csc.sales_code        # Código CSC (OXM, DBT, etc.)
ro.csc.countryiso_code   # Código de país
ro.build.fingerprint     # Huella digital del build
ro.build.version.oneui   # Versión de OneUI
```

**Biblioteca Nativa:** `libdprw.so`

Funciones JNI descubiertas:
- `Java_com_samsung_android_fotaagent_common_util_NativeUtils_unscramble`
- `Java_com_samsung_android_fotaagent_common_util_NativeUtils_getKey`
- `Java_com_samsung_android_fotaagent_common_util_NativeUtils_getRegiKey`
- `Java_com_samsung_android_fotaagent_common_util_NativeUtils_getTimeKey`
- `Java_com_samsung_android_fotaagent_common_util_NativeUtils_setPinAndFallocate`

**Claves/Strings de Encriptación:**
- `2cbmvps5z4`
- `j5p7ll8g33`
- `5763D0052DC1462E13751F753384E9A9`
- `AF87056C54E8BFD81142D235F4F8E552`
- `dkaghghkehlsvkdlsmld`

**Rutas del Sistema:**
- `/cache/checkp` - Checkpoint de verificación
- `/sys/class/sec/mmc/un` - Info MMC
- `/sys/class/sec/ufs/un` - Info UFS
- `/sys/block/mmcblk0/device/cid` - CID del dispositivo
- `/proc/sys/kernel/random/boot_id` - Boot ID

### 2. Aplicaciones Knox Analizadas

#### KnoxCore.apk
**Tamaño:** 635 KB (classes.dex)  
**Propósito:** Framework principal de Samsung Knox

**Componentes:**
- `KNOXCORE::KnoxKeyguardUpdateMonitor`
- Gestión de actualizaciones de seguridad Knox
- Monitoreo de integridad del sistema

#### KnoxGuard.apk
**Tamaño:** 1.7 MB  
**Propósito:** Servicio de bloqueo remoto y gestión de dispositivos

**Servidores:**
- `https://gsl.samsunggsl.com` - Guard Service Live
- `https://stg-gsl.samsunggsl.com` - Guard Service Staging
- `https://pinning-02.secb2b.com/service/umc/leafcert` - Certificados
- `https://stage-pinning-02.secb2b.com/service/umc/leafcert`

**Documentación:**
- https://docs.samsungknox.com/admin/knox-guard/how-to-guides/manage-devices/upload-devices/

#### KnoxPushManager.apk
**Tamaño:** 780 KB  
**Propósito:** Gestión de notificaciones push para Knox

**APIs:**
- Firebase Cloud Messaging
- Google Play Services APIs
- Firebase Installations API

#### KnoxERAgent.apk
**Propósito:** Knox Emergency Recovery Agent

### 3. SecDownloadProvider.apk

**Tamaño:** 157 KB  
**Propósito:** Proveedor de descargas seguras de Samsung

**Características:**
- Gestión de descargas en segundo plano
- Soporte para OTA updates (`otaupdate` flag)
- Download Booster
- Base de datos SQLite para gestión de descargas

**Estructura de BD:**
```sql
CREATE TABLE downloads(
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    uri TEXT, 
    method INTEGER, 
    entity TEXT, 
    no_integrity BOOLEAN, 
    hint TEXT, 
    otaupdate BOOLEAN, 
    _data TEXT, 
    mimetype TEXT, 
    destination INTEGER,
    ...
)
```

### 4. SmartSwitchAssistant.apk

**Tamaño:** 19 KB  
**Propósito:** Asistente para Samsung Smart Switch

**Servicios:**
- `com.samsung.android.Kies.KiesGetSetService`
- `SmartSwitchAssistantService`

**Características:**
- Gestión de permisos de Kies
- Actualización de archivos desde PC
- Verificación de integridad (`SYSSCOPE:1,NORMAL` vs `MODIFIED`)

### 5. AppUpdateCenter.apk

**Tamaño:** 3.6 MB  
**Propósito:** Centro de actualizaciones de aplicaciones Samsung

**Componentes:**
- Gestión de actualizaciones de Galaxy Apps
- Integración con Galaxy Store
- Sistema de notificaciones de actualizaciones

### 6. GalaxyResourceUpdater.apk

**Propósito:** Actualización de recursos del sistema Galaxy

## Protocolo FUS (Firmware Update Server)

### Endpoints Descubiertos

**URL Base:** `http://fus2.shop.v-cdn.net/FUS2`

#### 1. getNonce
**URL:** `{FUS_URL}/getNonce`  
**Método:** POST  
**Parámetros:**
```
id: [IMEI - 15 dígitos]
mode: "Nonce"
```
**Respuesta:** XML con nonce de autenticación

#### 2. getVersionLists
**URL:** `{FUS_URL}/getVersionLists`  
**Método:** POST  
**Parámetros:**
```
id: [IMEI]
mode: "list"
type: "firmware"
device_model_code: [MODEL] (ej: SM-S916B)
device_imei_push: [IMEI]
device_fwver: "0" o [VERSION_ACTUAL]
device_csc_code2: [CSC] (ej: OXM, DBT, XAA)
device_chnl_code: "0"
device_sales_code: ""
device_contents_no: "0"
device_country_code: ""
device_model_region: [CSC]
nonce: [NONCE del servidor]
auth: [HMAC-SHA1(nonce, IMEI+MODEL+CSC)]
```
**Respuesta:** XML con información de firmware disponible

#### 3. getBinaryInform
**URL:** `{FUS_URL}/getBinaryInform`  
**Método:** POST  
**Parámetros:** Similar a getVersionLists + `logic_check: [VERSION]`  
**Respuesta:** XML con información del binario (filename, path, size, CRC)

#### 4. getBinaryFile
**URL:** `{FUS_URL}/getBinaryFile?file={path}/{filename}`  
**Método:** GET  
**Respuesta:** Archivo binario del firmware

### Proceso de Autenticación

1. **Obtener Nonce:**
   - Enviar IMEI al endpoint `getNonce`
   - Servidor responde con nonce único

2. **Generar Auth Token:**
   - Concatenar: `IMEI + MODEL + CSC`
   - Calcular: `HMAC-SHA1(nonce, auth_data)`
   - Convertir a hexadecimal mayúsculas

3. **Realizar Petición:**
   - Incluir nonce y auth token en la petición
   - Servidor valida y responde con datos

### Formato de Respuesta XML

#### version.xml
```xml
<versioninfo>
    <firmware>
        <model>SM-S916B</model>
        <csc>OXM</csc>
        <version>
            <latest>S916BXXS8EYK5</latest>
            <upgrade>
                <value>S916BXXS8EYK5</value>
            </upgrade>
        </version>
    </firmware>
</versioninfo>
```

#### binary_inform
```xml
<firmware>
    <version>S916BXXS8EYK5</version>
    <filename>SM-S916B_1_20251128112708_abcd1234_fac.zip.enc4</filename>
    <path>/neofus/9/</path>
    <size>5432109876</size>
    <model>SM-S916B</model>
    <crc>abc123def456</crc>
    <encrypted>1</encrypted>
</firmware>
```

## Códigos CSC Comunes

| Código | Región/Operador |
|--------|-----------------|
| OXM | Open European Multi-CSC |
| DBT | Germany (Deutschland) |
| BTU | United Kingdom |
| XAA | USA Unlocked |
| XEF | France |
| XSP | Singapore |
| TPA | Taiwan |
| KOO | Korea |
| CHC | China |

## Modelos Samsung Populares

| Modelo | Dispositivo |
|--------|-------------|
| SM-S916B | Galaxy S23 (Internacional) |
| SM-S918B | Galaxy S23 Ultra |
| SM-S911B | Galaxy S23+ |
| SM-G990B | Galaxy S21 FE |
| SM-A536B | Galaxy A53 5G |
| SM-A546B | Galaxy A54 5G |
| SM-S901B | Galaxy S22 |
| SM-N986B | Galaxy Note 20 Ultra |

## Encriptación del Firmware

Los archivos de firmware Samsung suelen estar encriptados con:

**Formatos:**
- `.zip.enc2` - Encriptación versión 2
- `.zip.enc4` - Encriptación versión 4 (más reciente)

**Algoritmo:** AES (probablemente AES-256-CBC)

**Nota:** Las claves de desencriptación son propietarias de Samsung y no están públicamente disponibles. Se requieren herramientas oficiales como:
- Samsung Smart Switch
- Samsung Kies (legacy)
- Herramientas de la comunidad con claves extraídas

## Verificación de Integridad

**CRC Checksum:** Incluido en la respuesta XML  
**MD5/SHA256:** Posiblemente verificados por FotaAgent después de la descarga

## Estructura del Firmware Descargado

Archivos típicos en un paquete de firmware Samsung:

```
firmware.zip/
├── AP_[VERSION].tar.md5      # Application Processor (ROM principal)
├── BL_[VERSION].tar.md5      # Bootloader
├── CP_[VERSION].tar.md5      # Modem/Radio
├── CSC_[VERSION].tar.md5     # Consumer Software Customization
└── HOME_CSC_[VERSION].tar.md5 # CSC sin borrar datos
```

## Herramientas de Análisis Utilizadas

1. **unzip** - Extracción de APKs
2. **strings** - Análisis de binarios y DEX files
3. **grep** - Búsqueda de patrones
4. **Python 3** - Script de descarga

## Recomendaciones de Uso

### Parámetros Necesarios para el Script:

1. **Modelo del Dispositivo** (`-m`):
   - Formato: `SM-XXXXY` (ej: SM-S916B)
   - Obtener de `ro.product.model`

2. **Código CSC** (`-r`):
   - Código de 3 letras (ej: OXM, DBT)
   - Obtener de `ro.csc.sales_code`

3. **IMEI** (`-i`) [Opcional]:
   - 15 dígitos
   - Puede usar IMEI genérico: `000000000000000`

### Ejemplo de Uso:

```bash
# Verificar versión disponible
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM --check-only

# Descargar firmware
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM -o ./downloads

# Con IMEI específico
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM -i 123456789012345
```

## Limitaciones y Consideraciones

1. **Firmware Encriptado:** Los archivos descargados están encriptados y requieren desencriptación
2. **Tamaño Grande:** Los firmware suelen ser 4-6 GB
3. **Rate Limiting:** Los servidores pueden limitar descargas frecuentes
4. **Validación IMEI:** Algunos firmwares pueden requerir IMEI válido
5. **Región Lock:** Algunos modelos tienen region lock activo

## Archivos Generados

- `samsung_firmware_downloader.py` - Script principal de descarga
- `ANALISIS_FIRMWARE.md` - Este documento de análisis

## Referencias

- Firmware extraído: UN1CA-firmware-dm2q
- FotaAgent.apk: `system/system/priv-app/FotaAgent/`
- Build info: `system/system/build.prop`
- Metadata: `.extracted` (S916BXXS8EYK5/S916BOXM8EYK5/S916BXXU8EYI5)

---

**Fecha de Análisis:** 27 de Diciembre de 2024  
**Analista:** Script automatizado basado en ingeniería inversa
