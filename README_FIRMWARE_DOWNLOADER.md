# Samsung Firmware Downloader

## Descripción

Este script en Python permite descargar firmware oficial de Samsung (archivos `update.bin`) directamente desde los servidores FOTA (Firmware Over The Air) de Samsung. El script está basado en el análisis del APK `FotaAgent` y los binarios del sistema encontrados en el firmware de Samsung.

## Análisis del Proceso de Descarga

### Componentes Analizados

1. **FotaAgent.apk** (`system/system/priv-app/FotaAgent/`)
   - Aplicación principal de actualización de firmware
   - Gestiona la comunicación con servidores Samsung
   - Implementa el protocolo FOTA

2. **Protocolos de Comunicación**
   - **URL de verificación**: `https://fota-cloud-dn.ospserver.net/firmware/{region}/{model}/version.xml`
   - **URL de información binaria**: `https://neofussvr.sslcs.cdngc.net/NF_DownloadBinaryInform`
   - **URL de inicialización**: `https://neofussvr.sslcs.cdngc.net/NF_DownloadBinaryInitForMass`
   - **URL de descarga**: `http://cloud-neofussvr.sslcs.cdngc.net/NF_DownloadBinaryForMass`

3. **Autenticación**
   - Utiliza HMAC-SHA256 para generar un NONCE
   - Clave de autenticación: `hqzdurufm2c8mf6bsjezu1qgveouv7c7`
   - Requiere: IMEI, Modelo, Código CSC

### Proceso de Descarga

```
1. Cliente solicita información de firmware
   ↓
2. Genera NONCE con HMAC-SHA256(IMEI:MODELO:CSC)
   ↓
3. Envía petición XML a NF_DownloadBinaryInform
   ↓
4. Servidor responde con información del firmware
   ↓
5. Cliente inicializa descarga (NF_DownloadBinaryInitForMass)
   ↓
6. Cliente descarga el archivo binario
   ↓
7. Verifica integridad del archivo
```

## Requisitos

### Dependencias

```bash
pip install requests
```

### Información Necesaria

Para descargar firmware, necesitas:

1. **Modelo del dispositivo** (ejemplo: `SM-S916B`)
   - Puedes encontrarlo en: `build.prop` → `ro.product.system.model`
   - Para este firmware: `SM-S916B` (Galaxy S23+)

2. **Código CSC/Región** (ejemplo: `OXM`)
   - Define la región geográfica y el operador
   - Ejemplos comunes:
     - `OXM` - Open Europe (Multi-CSC)
     - `BTU` - United Kingdom
     - `DBT` - Germany (Deutschland)
     - `XEF` - France
     - `XAR` - USA AT&T
     - `TMB` - USA T-Mobile
     - `VZW` - USA Verizon

3. **IMEI** (opcional)
   - Identificador único de 15 dígitos
   - El script puede generar uno válido automáticamente
   - Formato: 15 dígitos con checksum Luhn válido

## Uso del Script

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/extremerom/UN1CA-firmware-dm2q.git
cd UN1CA-firmware-dm2q

# Instalar dependencias
pip install requests

# Hacer ejecutable el script
chmod +x samsung_firmware_downloader.py
```

### Uso Básico

```bash
# Descargar firmware más reciente
python samsung_firmware_downloader.py -m SM-S916B -r OXM

# Con IMEI personalizado
python samsung_firmware_downloader.py -m SM-S916B -r OXM -i 123456789012345

# Guardar en directorio específico
python samsung_firmware_downloader.py -m SM-S916B -r OXM -o /ruta/descargas

# Solo verificar disponibilidad (sin descargar)
python samsung_firmware_downloader.py -m SM-S916B -r OXM --check-only
```

### Parámetros del Script

| Parámetro | Descripción | Requerido | Ejemplo |
|-----------|-------------|-----------|---------|
| `-m, --model` | Modelo del dispositivo | Sí | `SM-S916B` |
| `-r, --region` | Código CSC/Región | Sí | `OXM` |
| `-i, --imei` | IMEI del dispositivo | No | `123456789012345` |
| `-v, --version` | Versión específica de firmware | No | `S916BXXS8EYK5` |
| `-o, --output` | Directorio de salida | No | `./downloads` |
| `--check-only` | Solo verificar, no descargar | No | - |

### Ejemplos Prácticos

#### 1. Descargar firmware para Galaxy S23+ Europa

```bash
python samsung_firmware_downloader.py -m SM-S916B -r OXM -o ./firmwares
```

#### 2. Verificar firmware disponible sin descargar

```bash
python samsung_firmware_downloader.py -m SM-S916B -r BTU --check-only
```

#### 3. Descargar firmware específico

```bash
python samsung_firmware_downloader.py -m SM-S916B -r OXM -v S916BXXS8EYK5
```

## Información del Dispositivo Actual

Basado en el firmware extraído (`S916BXXS8EYK5/S916BOXM8EYK5/S916BXXU8EYI5`):

- **Dispositivo**: Samsung Galaxy S23+ (dm2q)
- **Modelo**: SM-S916B
- **Versión Android**: 16 (Android Baklava)
- **Build ID**: BP2A.250605.031.A3
- **Versión de firmware**: S916BXXS8EYK5
- **CSC**: OXM (Open Europe)
- **Fecha de compilación**: Fri Nov 28 11:27:08 KST 2025
- **Parche de seguridad**: 2025-12-01

## Códigos CSC Comunes por Región

### Europa
- `OXM` - Open Europe (Multi-CSC) - **Recomendado**
- `BTU` - United Kingdom
- `DBT` - Germany
- `XEF` - France
- `ITV` - Italy
- `PHE` - Spain
- `SEB` - Baltic States
- `ATO` - Austria
- `SWC` - Switzerland
- `NEE` - Netherlands

### América
- `XAR` - USA (AT&T)
- `TMB` - USA (T-Mobile)
- `SPR` - USA (Sprint)
- `VZW` - USA (Verizon)
- `USC` - USA (US Cellular)
- `ACG` - USA (Unlocked)
- `ZTO` - Brazil
- `CHO` - Chile

### Asia
- `INS` - India
- `SIN` - Singapore
- `XSP` - Singapore
- `THL` - Thailand
- `SKC` - Korea (SK Telecom)
- `KTC` - Korea (KT)

### Oceanía
- `XSA` - Australia
- `PHN` - New Zealand

## Modelos Samsung Soportados

El script funciona con cualquier modelo Samsung que use FOTA:

### Serie Galaxy S
- `SM-S911B/U/N` - Galaxy S23
- `SM-S916B/U/N` - Galaxy S23+
- `SM-S918B/U/N` - Galaxy S23 Ultra
- `SM-S921B/U/N` - Galaxy S24
- `SM-S926B/U/N` - Galaxy S24+
- `SM-S928B/U/N` - Galaxy S24 Ultra

### Serie Galaxy A
- `SM-A546B/U` - Galaxy A54
- `SM-A556B/U` - Galaxy A55
- `SM-A346B/U` - Galaxy A34

### Serie Galaxy Z
- `SM-F936B/U` - Galaxy Z Fold 4
- `SM-F946B/U` - Galaxy Z Fold 5
- `SM-F731B/U` - Galaxy Z Flip 5

## Estructura del Archivo de Firmware

El archivo descargado (`update.bin` o similar) contiene:

1. **Particiones del sistema**:
   - `boot.img` - Kernel y ramdisk
   - `system.img` - Partición del sistema
   - `vendor.img` - Archivos del fabricante
   - `product.img` - Aplicaciones del producto
   - `odm.img` - Configuraciones ODM

2. **Metadatos**:
   - Información de versión
   - Checksums MD5/SHA
   - Configuración de particiones

## Solución de Problemas

### Error: "No firmware found"

**Causas posibles**:
- Modelo o región incorrectos
- Dispositivo no soportado
- Problemas de conectividad

**Solución**:
```bash
# Verificar que el modelo y región son correctos
python samsung_firmware_downloader.py -m SM-S916B -r OXM --check-only

# Intentar con diferentes códigos CSC
python samsung_firmware_downloader.py -m SM-S916B -r BTU --check-only
```

### Error: "Download failed"

**Solución**:
```bash
# Verificar conexión a internet
ping cloud-neofussvr.sslcs.cdngc.net

# Intentar nuevamente con timeout mayor
# Editar el script y aumentar timeout en requests
```

### Error: "Invalid IMEI"

**Solución**:
```bash
# Dejar que el script genere el IMEI automáticamente
python samsung_firmware_downloader.py -m SM-S916B -r OXM

# O usar un IMEI válido de 15 dígitos
python samsung_firmware_downloader.py -m SM-S916B -r OXM -i 359999001234567
```

## Notas de Seguridad

1. **IMEI**: El script puede generar un IMEI válido para consultas. No uses el IMEI real de tu dispositivo si no es necesario.

2. **Autenticación**: El script usa el protocolo oficial de Samsung FOTA, no realiza ningún tipo de hack o bypass.

3. **Firmware oficial**: Solo descarga firmware oficial de Samsung, verificado y firmado.

4. **Uso responsable**: Este script es para propósitos educativos y de desarrollo. Úsalo responsablemente.

## Análisis Técnico Detallado

### Formato de Petición XML

```xml
<FUSMsg>
  <FUSHdr>
    <ProtoVer>1.0</ProtoVer>
  </FUSHdr>
  <FUSBody>
    <Put/>
    <ACCESS_MODE>
      <Data>2</Data>
    </ACCESS_MODE>
    <NONCE>
      <Data>HMAC-SHA256(IMEI:MODEL:CSC)</Data>
    </NONCE>
    <MODEL_PATH>
      <Data>SM-S916B</Data>
    </MODEL_PATH>
    <DEVICE_IMEI_PUSH>
      <Data>123456789012345</Data>
    </DEVICE_IMEI_PUSH>
    <DEVICE_CSC_CODE2>
      <Data>OXM</Data>
    </DEVICE_CSC_CODE2>
  </FUSBody>
</FUSMsg>
```

### Formato de Respuesta XML

```xml
<FUSMsg>
  <FUSHdr>
    <ProtoVer>1.0</ProtoVer>
  </FUSHdr>
  <FUSBody>
    <Results>
      <RESULT_CODE>
        <Data>200</Data>
      </RESULT_CODE>
      <LATEST_FW_VERSION>
        <Data>S916BXXS8EYK5/S916BOXM8EYK5/S916BXXU8EYI5</Data>
      </LATEST_FW_VERSION>
      <BINARY_NAME>
        <Data>SM-S916B_1_20241128112708_xxx.zip.enc4</Data>
      </BINARY_NAME>
      <BINARY_SIZE>
        <Data>6442450944</Data>
      </BINARY_SIZE>
    </Results>
  </FUSBody>
</FUSMsg>
```

## Referencias

- Firmware actual: `S916BXXS8EYK5/S916BOXM8EYK5/S916BXXU8EYI5`
- Build: `BP2A.250605.031.A3`
- Android: 16 (Baklava)
- Dispositivo: Samsung Galaxy S23+ (dm2q/SM-S916B)

## Licencia

MIT License - Libre de usar con fines educativos y de desarrollo.

## Contribuciones

Para reportar problemas o contribuir mejoras:
1. Abre un issue en GitHub
2. Proporciona información detallada del problema
3. Incluye logs de error si es posible

## Autor

Generado a partir del análisis del firmware y APKs del sistema Samsung Galaxy S23+ (dm2q).
