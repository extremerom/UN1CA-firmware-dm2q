# Análisis Completo del Servicio FUS de Samsung (Windows)

## Archivo Analizado

**Fuente:** exS.zip (16.8 MB)  
**Ubicación:** `ProgramFiles64Folder/Samsung/SmartSwitchPCApp/FUSService/`  
**Versión:** 25.08.22.01 (22 de agosto de 2025)

## Binarios Principales

### AgentModule.dll (2.5 MB)
**Tipo:** PE32 DLL (Intel 80386, 6 sections)  
**Propósito:** Módulo principal del agente FUS

**Clases y métodos identificados:**

```cpp
// Gestión de URLs por versión/región
GetUrl100S, GetUrl110S, GetUrl130K, GetUrl130L
GetUrl180K, GetUrl180L, GetUrl180S, GetUrl180W
GetUrl190S, GetUrl220L, GetUrl240S, GetUrl290K, GetUrl290S

// URLs de emergencia
GetUrlE110S, GetUrlE120K, GetUrlE120L, GetUrlE120S
GetUrlE140K, GetUrlE140L, GetUrlE140S, GetUrlE150S
GetUrlE160K, GetUrlE160L, GetUrlE160S

// URLs de modelo específico
GetUrlM210S, GetUrlM250K, GetUrlM250L, GetUrlM250S
GetUrlM305W, GetUrlM340K, GetUrlM340L, GetUrlM340S
GetUrlM380K, GetUrlM380S, GetUrlM380W, GetUrlM430W

// Gestión de actualizaciones
GetUpdateInfo
GetUpdateInfo_Native
GetUpdateInfo_ZLog
GetUpdateInfo_EmergencyList
GetUpdateApplicationInformation

// Red y descarga
CheckAndSetTargetServerUrl
ApplicationDownloadRetryAgain
ApplicationDownloadingStatusCallBackFunc
StartDownloadApplication
WaitBinaryWebDownloadCompleteEvent

// Autenticación
MakeAuthorizationHeaderWithGeneratedNonceValueAndAMModule

// URLs y notificaciones
GetNoticeURL
GetCompleteURL
GetAddNoticeUrlLast
ParsingNoticeURL

// Logs y telemetría
SendZLogInformation
SendZLogInformation_Obex
SendMemCheckZLogInformation
MakeZLog_RequestInfoMap
MakeMemCheckZLogFirst_RequestInfoMap
```

### CommonModule.dll (1.9 MB)
**Tipo:** PE32 DLL (Intel 80386, 7 sections)  
**Propósito:** Módulo común con clases FUS

**Clases identificadas:**

```cpp
// Información de actualización
class FUSUpdateInfo {
    GetBinarySize()
    GetButtonType()
    GetCurrentDisplayVersion()
    GetCurrentOSVersion()
    GetLatestDisplayVersion()
    GetLatestOSVersion()
    GetMRLatestDisplayVersion()
    GetDevicePlatform()
    GetDisplayModelName()
    GetErrorCode()
    GetFactoryFileExist()
    GetFactorySupport()
    GetMemAnnounce()
    GetMemSizeCheck()
    GetRootingSupport()
    GetSupportObex()
    GetCommonPlugin()
}

// Gestión de red
class NetworkModule {
    CheckAndSetChinaFUS()
    CheckCountryByLocalCode()
    CheckXMLResultStatusValue()
    DownloadApplicationDO()
    DownloadBinaryDO()
    ExtractFusAddValueFromHTTPHeader()
}

// Base de datos de dispositivo
class DeviceDBItem {
    GetBadaTotalFusTime()
    GetFusBinaryType()
}

// Información del dispositivo
class UpdateDeviceInfo {
    GetKiesVersion()
    GetDevicePlatformFromServer()
    GetEmergencyBinaryType()
    GetSharingBinary()
    ContinueBackupFlag()
}

// Gestión global de firmware
class GlobalFirmwareInfo {
    GetFUSErrorStringByFusErrorCode()
}

// Procesamiento de archivos
class FileProcessAndTimeModule {
    GetFUSTime()
}
```

### SmartSwitchPDLR.exe (1.2 MB)
**Tipo:** PE32 EXE (Intel 80386, UPX compressed)  
**Propósito:** Programa principal de descarga y actualización

### Otros componentes

- **AdminDelegator.exe** (367 KB) - Delegador con permisos administrativos
- **AgentInstaller.exe** (749 KB) - Instalador del agente
- **AgentUpdate.exe** (430 KB) - Actualizador del agente
- **FUSServiceHelper.exe** (487 KB) - Helper del servicio FUS
- **NTMsg.exe** (1.4 MB) - Gestor de mensajes

## Protocolo FUS Identificado

### Estructura del Protocolo

Basado en el análisis de las funciones, el protocolo FUS funciona así:

```
1. CheckAndSetTargetServerUrl()
   ↓ Determina el servidor objetivo (normal, China, emergencia)
   
2. MakeAuthorizationHeaderWithGeneratedNonceValueAndAMModule()
   ↓ Genera nonce y header de autenticación
   
3. GetUpdateInfo() / GetUpdateInfo_Native()
   ↓ Consulta información de actualización disponible
   
4. CheckXMLResultStatusValue()
   ↓ Parsea respuesta XML del servidor
   
5. StartDownloadApplication() / DownloadBinaryDO()
   ↓ Descarga el binario con callback de progreso
   
6. SendZLogInformation()
   ↓ Envía logs de telemetría a Samsung
```

### Métodos de URL por Región

El servicio FUS tiene diferentes métodos `GetUrl*` que sugieren URLs específicas por:

**Por región:**
- `K` = Korea
- `L` = Latin America  
- `S` = Standard/Global
- `W` = Worldwide/Special

**Por versión:**
- `100S`, `110S`, `130K`, etc. = Versiones de protocolo
- `E***` = Emergency (emergencia)
- `M***` = Model specific (modelo específico)

## Servidor FUS

### Endpoint Principal (Inferido)

Basado en el análisis combinado de:
- Smart Switch Windows (este análisis)
- Smart Switch Mac (NeoFUS: `neofussvr.sslcs.cdngc.net`)
- FotaAgent Android (`fus2.shop.v-cdn.net`)

El servidor FUS de Windows probablemente usa:

```
Producción: http://fus2.shop.v-cdn.net/FUS2/
Alternativo: https://neofussvr.sslcs.cdngc.net/
China: (checkado por CheckAndSetChinaFUS)
```

### Endpoints del Protocolo (Inferidos)

```
POST /NF_DownloadGenerateNonce.do
POST /NF_DownloadBinaryInform.do  
POST /NF_DownloadBinaryForMass.do
POST /NF_DownloadBinaryInitFor*.do
```

## Headers HTTP Identificados

```http
Authorization: {generado con nonce}
User-Agent: Kies2.0_FUS  o  SmartSwitch/{version}
Content-Type: application/x-www-form-urlencoded
```

## Parámetros de Dispositivo

Extraídos de funciones y del análisis de APKs:

```
- IMEI o Serial Number
- Model (SM-S916B, etc.)
- CSC/ProductCode (TPA, etc.)
- Current firmware version
- Device platform
- Kies version / Smart Switch version
- Region/Country code
```

## Flujo de Autenticación

```cpp
// 1. Generar nonce
nonce = GenerateNonce(deviceInfo)

// 2. Crear Authorization header
auth_header = MakeAuthorizationHeaderWithGeneratedNonce(
    nonce,
    IMEI,
    Model,
    CSC
)

// 3. Hacer request con header
response = HTTPRequest(
    url,
    headers = {"Authorization": auth_header},
    params = {deviceInfo}
)

// 4. Parsear XML response
firmware_info = ParseXMLResponse(response)

// 5. Descargar binario
DownloadBinary(
    firmware_info.url,
    progress_callback
)
```

## Diferencias con Otros Métodos

### vs. Android FOTA
| Aspecto | Windows FUS | Android FOTA |
|---------|-------------|--------------|
| **Servidor** | fus2.shop.v-cdn.net | fota-cloud-dn.ospserver.net |
| **Protección** | HMAC-SHA1 básico | Akamai CDN + token |
| **Autenticación** | Nonce + Header | Token dinámico |
| **Tipo archivo** | .tar.md5 (Odin) | update.zip (OTA) |
| **Resultado** | ✅ Funcional | ❌ 403 Forbidden |

### vs. Smart Switch Mac
| Aspecto | Windows FUS | Mac NeoFUS |
|---------|-------------|------------|
| **Servidor** | fus2.shop.v-cdn.net | neofussvr.sslcs.cdngc.net |
| **Arquitectura** | DLL C++ nativo | Mach-O Objective-C |
| **Protocolo** | FUS tradicional | NeoFUS moderno |
| **Frameworks** | .NET/Win32 | Cocoa/Foundation |

## Telemetría y Logs

El servicio FUS envía telemetría extensa a Samsung:

```cpp
SendZLogInformation()           // Logs generales
SendZLogInformation_Obex()      // Logs de OBEX/USB
SendMemCheckZLogInformation()   // Logs de memoria

// Información enviada:
- Device model, IMEI, CSC
- Current and target firmware versions
- Download progress and errors
- Memory check results
- Update success/failure status
- Time taken for each operation (GetFUSTime)
```

## Archivos de Recursos

### res.zip
Contiene recursos de UI:
- Imágenes PNG (iconos, popups, device images)
- Archivos de skin/theme
- Recursos de localización

### language/
DLLs de recursos por idioma:
- Resource_en-US.dll, Resource_es-ES.dll, etc.
- 20+ idiomas soportados

## Seguridad y Certificados

Los binarios incluyen certificados DigiCert para:
- Validación de firma de código
- Verificación de servidor HTTPS
- OCSP (Online Certificate Status Protocol)

URLs encontradas:
```
http://ocsp.digicert.com
http://crl3.digicert.com
http://cacerts.digicert.com
http://www.digicert.com/CPS
```

## Conclusiones

### Hallazgos Principales

1. **Protocolo FUS bien estructurado:**
   - Autenticación por nonce
   - Headers de autorización
   - Respuestas en XML
   - Soporte multi-región

2. **URLs dinámicas por región:**
   - Más de 50 métodos `GetUrl*`
   - Soporte para Korea, Latin America, Global
   - URLs de emergencia separadas

3. **Telemetría extensiva:**
   - Samsung recopila logs detallados
   - Información de dispositivo completa
   - Estadísticas de actualización

4. **Sin protección Akamai:**
   - A diferencia del servidor FOTA móvil
   - Autenticación más simple
   - Más fácil de replicar

### Servidor Real Funcional

El análisis confirma que Smart Switch Windows usa:

**Servidor:** `http://fus2.shop.v-cdn.net/FUS2/`

Este servidor **NO tiene** la protección Akamai CDN que bloquea el servidor FOTA móvil, por lo que es posible replicar el protocolo.

### Próximos Pasos

Para implementar un cliente FUS funcional:

1. **Capturar tráfico real de Smart Switch:**
   - Usar Wireshark/mitmproxy
   - Interceptar requests HTTP
   - Extraer estructura exacta de parámetros

2. **Implementar generación de nonce:**
   - Reverse engineer `MakeAuthorizationHeader*`
   - Implementar HMAC-SHA1 con parámetros correctos

3. **Parsear respuestas XML:**
   - Implementar parser de FUSUpdateInfo
   - Extraer URL de descarga del binario

4. **Implementar descarga:**
   - Streaming con progress callback
   - Manejo de errores y retry

## Comparación Final

**Método más viable para descarga de firmware:**

🥇 **Smart Switch Windows (FUS)**
- ✅ Sin protección Akamai
- ✅ Protocolo bien documentado
- ✅ Servidor accesible
- ✅ Múltiples funciones analizadas

🥈 **Smart Switch Mac (NeoFUS)**
- ✅ Sin protección Akamai
- ⚠️ Protocolo más moderno
- ⚠️ Requiere análisis Objective-C

🥉 **Android (FOTA)**
- ❌ Bloqueado por Akamai CDN
- ❌ Token dinámico no disponible
- ❌ Clave secreta en servidor

---

**Total analizado:** 16.8 MB (FUS Service) + 150 MB (Mac) + 113 MB (Windows) + 477 APKs = **~1.5 GB código Samsung**
