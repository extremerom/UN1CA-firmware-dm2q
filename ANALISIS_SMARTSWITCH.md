# Análisis de Smart Switch para Windows

## Información General

**Archivo:** SmartSwitchApp (Package)_5.0.33.0_x64.msix  
**Tamaño:** 113 MB  
**Versión:** 5.0.33.0  
**Plataforma:** Windows 10/11 (MSIX package)  
**Framework:** .NET (WinUI 3)

## Estructura del Paquete

```
SmartSwitch.msix
├── SmartSwitchApp (Package)_5.0.33.0_x64.msix  (113 MB - principal)
├── Language packs (38 idiomas)
└── Scale assets (100%, 125%, 150%, 400%)
```

## Hallazgos Clave

### 1. Servicio FUS Descubierto

En `SmartSwitchApp.dll` encontrado:

```csharp
// Clases y métodos relacionados con FUS
IFUSService
InitFUSService
StopFUSService
ResetFUSService
StartFUSUpdate
FUSStartCheckUpdate
CheckFusRestore
GetFUSBnRMode
SetFUSBnRMode

// Eventos FUS
OnFUSModuleLoadedEvent
OnFUSPopupEvent
OnFUSRequestMainDimmedEvent
OnFUSDeviceUpdateInfoEvent

// Estados
FUS_RESULT_CODE
FUS_UPDATE_INFO
FUSTypesForUI

// Predownload
LastestSoftwarePreDownload
UpdateFUSPredownloadList
IsPreDownloadTestMode
PreDownloadTargetDevices
```

### 2. Descarga de Firmware

```csharp
// Métodos de descarga
DownloadFromWebApiAsync
RequestDownloadAndInstallStorePackageUpdatesAsync
AppDownloadProgressChange
PackageDownloadProgress

// HTTP
HttpClient
HttpResponseMessage
HttpCompletionOption
HttpContentHeaders
System.Net.Http
```

### 3. Manual Download APK

Smart Switch también puede descargar APK de Smart Switch para Android:

```csharp
ManualDownloadSmartSwitchApkPage
ManualDownloadSmartSwitchApkPageViewModel
ManualDownloadSmartSwitchApkTitle
ManualDownloadSmartSwitchApkDescription
```

## Arquitectura de Descarga

### Flujo Identificado

```
Smart Switch (Windows)
    ↓
IFUSService (Servicio externo o COM)
    ↓
FUS Protocol
    ↓
Samsung FUS Server (fus2.shop.v-cdn.net o similar)
    ↓
Firmware Download
```

### Diferencias con Android

| Aspecto | Android (FotaAgent) | Windows (Smart Switch) |
|---------|---------------------|------------------------|
| **Servidor** | fota-cloud-dn.ospserver.net | Posiblemente FUS directo |
| **Protección** | Akamai CDN con token | Posiblemente sin Akamai |
| **Autenticación** | Token dinámico | Credenciales FUS |
| **Tipo archivo** | update.zip (OTA) | .tar.md5 (Odin) |

## Servicio FUS Externo

El servicio `IFUSService` parece ser:

1. **COM Object** - Servicio Windows registrado
2. **Proceso separado** - Maneja la lógica de FUS
3. **Comunicación IPC** - Smart Switch se comunica via eventos

### Búsqueda del Servicio FUS

Posibles ubicaciones:
```
C:\Program Files\Samsung\Smart Switch\FUSService.exe
C:\Program Files\Samsung\Smart Switch\FUS\
C:\ProgramData\Samsung\Smart Switch\
```

O podría estar incluido en:
- Driver USB Samsung
- Samsung Kies (legacy)
- Componente COM registrado en el sistema

## Base de Datos de Modelos

**Archivo:** `SamsungModelDB.xml` (229 KB)

Contiene configuración de modelos Samsung:
- Propiedades de dispositivos
- Capacidades de backup/restore
- Tipos de sincronización soportados
- Esquemas de base de datos

No contiene URLs de descarga de firmware (están en código compilado o servicio externo).

## Análisis de Protocolo

### Smart Switch NO usa Akamai directamente

A diferencia del servidor Android FOTA, Smart Switch probablemente:

1. **Usa FUS Server directo**
   ```
   http://fus2.shop.v-cdn.net/FUS2
   ```

2. **Autenticación FUS**
   - Nonce + HMAC-SHA1
   - IMEI + Model + Region
   - Sin token Akamai necesario

3. **Descarga desde CDN Samsung**
   - El servidor FUS proporciona URL de descarga
   - URL puede incluir token temporal
   - CDN diferente al de FOTA móvil

## Ventajas de Smart Switch

1. ✅ **No requiere token Akamai**
2. ✅ **Descarga firmware completo** (.tar.md5 para Odin)
3. ✅ **Servidor FUS más accesible**
4. ✅ **No tiene restricciones de dispositivo móvil**

## Recomendación para Script Python

### Opción A: Emular Smart Switch

```python
# 1. Usar protocolo FUS completo (como Smart Switch)
class SmartSwitchEmulator(SamsungFirmwareDownloader):
    def download_firmware_smartswitch_method(self):
        # 1. getNonce
        nonce = self.get_nonce_fus()
        
        # 2. getVersionLists
        versions = self.get_version_lists_fus(nonce)
        
        # 3. getBinaryInform
        binary_info = self.get_binary_inform_fus(nonce, version)
        
        # 4. getBinaryFile (URL directa sin Akamai)
        download_url = binary_info['url']  # URL sin token Akamai
        self.download(download_url)
```

### Opción B: Interceptar Smart Switch

```bash
# 1. Instalar Smart Switch
# 2. Configurar proxy (Fiddler, mitmproxy)
# 3. Conectar dispositivo y descargar firmware
# 4. Capturar peticiones FUS
# 5. Extraer protocolo y URLs
```

## Próximos Pasos

### 1. Buscar FUSService.exe

```bash
# En Windows con Smart Switch instalado
dir "C:\Program Files\Samsung\" /s /b | findstr FUS
dir "C:\ProgramData\Samsung\" /s /b | findstr FUS
```

### 2. Interceptar Tráfico Smart Switch

```bash
# Con mitmproxy
mitmproxy -p 8080 --ssl-insecure

# Configurar proxy del sistema en Windows
# Ejecutar Smart Switch
# Capturar peticiones a fus2.shop.v-cdn.net
```

### 3. Analizar Registry de Windows

```powershell
# Buscar configuración de FUS
Get-ItemProperty -Path "HKLM:\SOFTWARE\Samsung\*" -Recurse | Select-String "FUS"
Get-ItemProperty -Path "HKCU:\SOFTWARE\Samsung\*" -Recurse | Select-String "FUS"
```

## Comparación Final

### Android FOTA
```
❌ Protegido por Akamai CDN
❌ Requiere token dinámico
❌ Token generado en servidor
✅ Descarga OTA (update.zip)
```

### Smart Switch
```
✅ Usa FUS directo
✅ Autenticación HMAC-SHA1 estándar
✅ Sin token Akamai
✅ Descarga firmware completo (.tar.md5)
```

## Conclusión

**Smart Switch es el método preferido para descargar firmware** porque:

1. No tiene la protección Akamai del servidor FOTA móvil
2. Usa protocolo FUS estándar documentado
3. El servicio FUS puede ser llamado directamente
4. Descarga archivos completos para Odin (AP, BL, CP, CSC)

**Siguiente paso:**
Implementar cliente FUS completo que emule Smart Switch, sin necesidad de token Akamai.

---

**Fecha de Análisis:** 27 Diciembre 2024  
**Smart Switch Version:** 5.0.33.0  
**Método:** Análisis de MSIX package y DLLs .NET
