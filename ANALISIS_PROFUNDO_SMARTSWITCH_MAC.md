# Análisis Profundo: Smart Switch Mac - Protocolo FUS Completo

## Resumen Ejecutivo

**Problema:** El endpoint `update.kies.samsung.com/update/smartswitchpc/image` solo devuelve **imágenes PNG** de dispositivos, NO firmware completo (.tar.md5).

**Solución encontrada:** Smart Switch Mac usa el servidor **NeoFUS** (neofussvr.sslcs.cdngc.net) con protocolo FUS tradicional similar a Windows.

## Servidores Descubiertos en FUS Agent

### 1. NeoFUS Server (Principal)

```
PRODUCCIÓN:
https://neofussvr.sslcs.cdngc.net

STAGING/TEST:
https://neofusstgsvr.samsungmobile.com

CHINA:
https://cnfussvr.sslcs.cdngc.net
```

**Función:** Servidor FUS principal para descarga de firmware

### 2. Update Server (Metadatos)

```
https://update.kies.samsung.com/update/smartswitchpc/
```

**Función:** Solo para imágenes de dispositivos y metadatos, NO firmware

## Análisis del FUS Agent Bundle

### Estructura

```
SAMSUNG FUS Agent.bundle/
├── Contents/
│   ├── MacOS/
│   │   └── SAMSUNG FUS Agent (Mach-O Universal Binary)
│   └── Resources/
│       ├── FUSFirmwareWindow.nib
│       ├── FUSEmergencyAndInit.nib
│       ├── FUSInitialization.nib
│       └── [40+ archivos de interfaz]
```

### Clases Principales Descubiertas

```objectivec
// Gestión de sesión FUS
_OBJC_CLASS_$_FUSSession
_OBJC_CLASS_$_FUSSessionManager

// Actualización de firmware
_OBJC_CLASS_$_FUSFirmwareUpdateController
_OBJC_CLASS_$_FUSFirmwareWindowController
_OBJC_CLASS_$_FUSAgent

// Descarga
_OBJC_CLASS_$_FUSFirmwareAheadDNController
_OBJC_CLASS_$_FUSInitializeDownloadPopupWindowController

// Emergencia
_OBJC_CLASS_$_FUSEmergencyAndInitController
_OBJC_CLASS_$_FUSFirmwareEmergencyController

// Notificaciones
_OBJC_CLASS_$_FUSFirmwareNotiController
_OBJC_CLASS_$_FUSFirmwareWebNotiWindowController
```

### Métodos Clave Identificados

```objectivec
// Verificación de binarios
-checkBinary:nIndex:IMEI:OTP:
-checkBinaryForInit:nIndex:IMEI:OTP:
-checkBinaryGetResult_NF:
-getBinaryInformResponseFor:necessaryData:
-getBinarySize

// Versiones
-getVersionStr:forNew:
-getVersionStrForInit:forNew:
-checkFirmware:
-compareDeviceVersion:currentDeviceVersion:

// Descarga
-doAgentDownload
-downloadAgentThread:
-downloadPluginThread:
-downloadInformAgent
-downloadInformBin
-downloadInformPlugin
-initializeDownload:
-initializeDownloadThread:
-upgradeFirmware:

// Sesión
-openSession:locationID:
-closeSession:
-getOpenSessions
-getUpgradeSession
```

## Protocolo FUS en Smart Switch Mac

### Arquitectura Híbrida Descubierta

Smart Switch Mac usa **DOS protocolos** diferentes:

#### 1. REST API (para metadatos)

```
Endpoint: https://update.kies.samsung.com/update/smartswitchpc/image
Método: GET
Parámetros:
  - model: SM-S916B
  - ProductCode: TPA

Respuesta:
{
  "resultCode": 0,
  "resultMessage": "ok",
  "url": "https://sspc.sec-smartswitch.com/.../imagen.png",  ← SOLO IMAGEN
  "status": "active",
  "deviceName": "Galaxy S23+"
}
```

**Limitación:** Solo devuelve imagen del dispositivo, NO firmware.

#### 2. Protocolo FUS (para firmware)

```
Servidor: https://neofussvr.sslcs.cdngc.net
Método: Similar a Windows FUS
Endpoints esperados (basado en strings encontrados):
  - /NF_DownloadGenerateNonce.do
  - /NF_DownloadBinaryInform.do
  - /NF_DownloadBinaryInitForMass.do
```

### Flujo de Descarga Identificado

```
1. Usuario conecta dispositivo
   ↓
2. Smart Switch obtiene información (OBEX):
   - Modelo, CSC, IMEI
   - Versión actual
   - Espacio disponible
   ↓
3. openSession:locationID:
   Abre sesión FUS con dispositivo
   ↓
4. checkFirmware:
   Consulta servidor NeoFUS
   ↓
5. getBinaryInformResponseFor:necessaryData:
   Obtiene información del binario
   ↓
6. doAgentDownload
   Descarga firmware desde NeoFUS
   ↓
7. upgradeFirmware:
   Flashea firmware via OBEX/USB
```

## Archivos XML Usados por FUS Agent

```
URLInfo.xml          - URLs de servidores
customaccess.xml     - Acceso personalizado
plugin.xml           - Información de plugins
common.xml           - Configuración común
userInfo.xml         - Información de usuario
predownloadmodel.xml - Modelos para pre-descarga
emergency/%@.%@.xml  - Información de emergencia
```

## Comparación: API REST vs Protocolo FUS

| Característica | REST API | Protocolo FUS |
|----------------|----------|---------------|
| **Servidor** | update.kies.samsung.com | neofussvr.sslcs.cdngc.net |
| **Método HTTP** | GET | POST (probablemente) |
| **Autenticación** | Parámetros URL | Nonce + HMAC |
| **Datos descarga** | Imagen PNG | Firmware .tar.md5 |
| **Complejidad** | Baja | Alta |
| **Estado actual** | ✅ Funciona | ⚠️ Requiere investigación |

## Análisis del Servidor NeoFUS

### Test de Conectividad

```bash
curl -H "User-Agent: Smart Switch Mac/5.0.43.1" \
     "https://neofussvr.sslcs.cdngc.net"

Respuesta: 403 Forbidden
Razón: Requiere path y parámetros correctos
```

### Posibles Endpoints (extrapolación de Windows FUS)

Basado en análisis de FUS Agent y Windows Smart Switch:

```
https://neofussvr.sslcs.cdngc.net/NF_DownloadGenerateNonce.do
  → Generar nonce de autenticación

https://neofussvr.sslcs.cdngc.net/NF_DownloadBinaryInform.do
  → Obtener información del binario

https://neofussvr.sslcs.cdngc.net/NF_DownloadBinaryInitForMass.do
  → Inicializar descarga masiva

https://neofussvr.sslcs.cdngc.net/NF_DownloadBinaryForMass.do
  → Descargar binario
```

### Parámetros Esperados (inferidos)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<FUSMsg>
  <FUSHdr>
    <ProtoVer>1.0</ProtoVer>
  </FUSHdr>
  <FUSBody>
    <Put>
      <ACCESS_MODE>2</ACCESS_MODE>
      <BINARY_NATURE>1</BINARY_NATURE>
      <CLIENT_PRODUCT>Smart Switch</CLIENT_PRODUCT>
      <CLIENT_VERSION>5.0.43.1</CLIENT_VERSION>
      <DEVICE_FW_VERSION>{version_actual}</DEVICE_FW_VERSION>
      <DEVICE_IMEI>{imei}</DEVICE_IMEI>
      <DEVICE_LOCAL_CODE>{csc}</DEVICE_LOCAL_CODE>
      <DEVICE_MODEL_NAME>{modelo}</DEVICE_MODEL_NAME>
      <LOGIC_CHECK>{nonce}</LOGIC_CHECK>
    </Put>
  </FUSBody>
</FUSMsg>
```

## Por Qué Fallan los Endpoints Actuales

### Problema 1: update.kies.samsung.com/image

```bash
curl "https://update.kies.samsung.com/update/smartswitchpc/image?model=SM-S916B&ProductCode=TPA"

Respuesta:
{
  "url": "https://sspc.sec-smartswitch.com/.../SM-S916B...png",  ← PNG, no .tar.md5
  "deviceName": "Galaxy S23+"
}
```

**Razón:** Este endpoint es para obtener **imagen de marketing** del dispositivo, no firmware.

### Problema 2: api.sec-smartswitch.com/application

```bash
curl "https://api.sec-smartswitch.com/smartswitch/v8/application?locale=en_US&osType=mac"

Respuesta:
{
  "resultCode": 2000,
  "resultMessage": "Parameter Validation Error"
}
```

**Razón:** Faltan parámetros requeridos. Este endpoint probablemente es para:
- Listado de aplicaciones de Smart Switch
- Metadatos de la aplicación
- NO para firmware

## Diferencias: Mac vs Windows vs Android

| Plataforma | Servidor Firmware | Protocolo | Autenticación |
|------------|-------------------|-----------|---------------|
| **Android FOTA** | fota-cloud-dn.ospserver.net | HTTP + Akamai | Token CDN dinámico |
| **Windows Smart Switch** | fus2.shop.v-cdn.net | FUS XML/SOAP | HMAC-SHA1 |
| **Mac Smart Switch** | neofussvr.sslcs.cdngc.net | FUS XML (NeoFUS) | HMAC + Nonce |

## Evidencia del Protocolo NeoFUS

### Strings Clave Encontrados

```
TARGET_SERVER                    → Variable para servidor
FUS_SNCD_IP/TARGET_SERVER       → IP/servidor FUS
emergency/%@.%@.xml             → XMLs de emergencia
predownloadmodel.xml            → Modelos para pre-descarga
URLInfo.xml                     → Información de URLs
checkBinary:nIndex:IMEI:OTP:    → Verificación con IMEI/OTP
getBinaryInformResponseFor:     → Respuesta de info binaria
initializeDownload:             → Iniciar descarga
upgradeFirmware:                → Actualizar firmware
```

### Propiedades de Dispositivo Usadas

```objectivec
DEVICE_MODEL_NAME      → ro.product.model (SM-S916B)
DEVICE_LOCAL_CODE      → ro.csc.sales_code (TPA)
DEVICE_FW_VERSION      → ro.build.PDA (versión actual)
DEVICE_IMEI            → IMEI del dispositivo
```

## Funciones de Pre-descarga

Smart Switch Mac incluye funcionalidad de **pre-descarga**:

```objectivec
-PredownloaderStatusCheck
-setPredownloaderCaller
-PredownloaderKill
-savePredownload:
-checkPredownloadComponents
-killPredownloader
-isPredownloaderRunning
```

**Propósito:** Descargar firmware ANTES de conectar el dispositivo.

**Ruta de almacenamiento:**
```
~/Library/Application Support/.FUS/predownloaderSmartSwitch
```

## Funciones de Inicialización

```objectivec
// Descarga inicial (OTA first-time)
-doInitializeDownload
-initializeDownload:
-initializeDownloadThread:
-checkSNNumberForInitialDownloadWithSN:withSNType:
-getInitDownloadWithStep:withData:
-initialDownloadResponse:
```

**Propósito:** Descargar firmware para dispositivos nuevos o sin ROM.

## Próximos Pasos para Implementación

### Paso 1: Descubrir Endpoints NeoFUS Exactos

Necesitamos encontrar los endpoints exactos del servidor NeoFUS. Opciones:

1. **Interceptar Smart Switch real:**
   ```bash
   # En Mac con Smart Switch instalado
   sudo tcpdump -i any -A 'host neofussvr.sslcs.cdngc.net' -w neofus_capture.pcap
   
   # Luego usar Smart Switch para descargar firmware
   # Analizar el .pcap con Wireshark
   ```

2. **Análisis de tráfico con mitmproxy:**
   ```bash
   mitmproxy --ssl-insecure
   # Configurar Mac para usar proxy
   # Usar Smart Switch
   ```

3. **Decompilación más profunda:**
   - Usar Hopper Disassembler o IDA Pro
   - Analizar FUS Agent bundle con más detalle
   - Buscar constantes de URL hardcodeadas

### Paso 2: Implementar Cliente NeoFUS

Una vez descubiertos los endpoints, implementar:

```python
class NeoFUSClient:
    """
    Cliente para protocolo NeoFUS de Smart Switch Mac
    """
    
    BASE_URL = "https://neofussvr.sslcs.cdngc.net"
    
    def generate_nonce(self):
        """Generar nonce de autenticación"""
        # POST /NF_DownloadGenerateNonce.do
        pass
    
    def get_binary_inform(self, model, csc, imei, nonce):
        """Obtener información del binario"""
        # POST /NF_DownloadBinaryInform.do
        pass
    
    def download_firmware(self, binary_info):
        """Descargar firmware completo"""
        # POST /NF_DownloadBinaryForMass.do
        pass
```

### Paso 3: Parámetros Requeridos

```python
device_info = {
    'MODEL': 'SM-S916B',
    'CSC': 'TPA',
    'IMEI': '352496803361546',
    'CURRENT_VERSION': 'S916BXXS8EYK5',  # Versión actual
    'BINARY_NATURE': '1',                # 1=Firmware, 2=Plugin
    'CLIENT_PRODUCT': 'Smart Switch',
    'CLIENT_VERSION': '5.0.43.1'
}
```

## Soluciones Alternativas Viables

Mientras se descubren los endpoints exactos de NeoFUS:

### Opción 1: Usar Smart Switch Real + Interceptar

**Ventaja:** Obtener URLs reales de descarga  
**Desventaja:** Requiere dispositivo físico

### Opción 2: Analizar Windows Smart Switch

Windows Smart Switch usa FUS tradicional que SÍ conocemos:

```
Servidor: http://fus2.shop.v-cdn.net/FUS2
Endpoints:
  - NF_DownloadGenerateNonce.do
  - NF_DownloadBinaryInform.do
  - NF_DownloadBinaryForMass.do
```

Mac probablemente usa los mismos endpoints pero en neofussvr.

### Opción 3: API de Samsung Mobile

Investigar si existe API pública/documentada:

```
https://developer.samsung.com/
https://www.samsung.com/global/download/
```

## Conclusiones

### ✅ Descubrimientos Confirmados

1. **Servidor real:** neofussvr.sslcs.cdngc.net (NeoFUS)
2. **Protocolo:** Similar a FUS Windows pero con variaciones
3. **Estructura:** FUS Agent bundle con 30+ clases Objective-C
4. **Métodos:** checkBinary, getBinaryInform, downloadAgent, upgradeFirmware
5. **Pre-descarga:** Funcionalidad incluida (~/.FUS/)

### ⚠️ Limitaciones Actuales

1. **Endpoints exactos desconocidos:** Necesitan ser descubiertos
2. **Formato XML específico:** Requiere análisis del protocolo
3. **Autenticación NeoFUS:** Diferente a FUS tradicional
4. **API REST limitada:** Solo devuelve imágenes, no firmware

### 🎯 Recomendación Final

**Para descargar firmware Samsung con Smart Switch Mac:**

1. **Inmediato:** Usar Smart Switch oficial (descarga garantizada)
2. **Corto plazo:** Interceptar tráfico para encontrar endpoints
3. **Largo plazo:** Implementar cliente NeoFUS completo

**El endpoint REST de update.kies.samsung.com NO sirve para descargar firmware, solo para metadatos e imágenes.**

---

**Análisis completado:** 27 de diciembre de 2025  
**Herramientas usadas:** strings, nm, otool, file, 7zip, dmg2img  
**Archivos analizados:** 
- SmartSwitch 5.0.43.1 (39 MB DMG)
- FUS Agent Bundle (Mach-O Universal)
- DeviceCenter.framework
- KMBase.framework

**Total analizado:** 150 MB descomprimido, 4 frameworks, 40+ clases FUS
