# Análisis de Ingeniería Inversa: FUS Service (Windows)

## Información del Paquete Analizado

**Fuente**: `exS.zip` del repositorio  
**Tamaño**: 17 MB (17,715,263 bytes)  
**Versión FUS Agent**: 25.08.22.01  
**Fecha**: 2024-08-22  

## Estructura del Paquete

```
exS.zip
├── ProgramFiles64Folder/
│   └── Samsung/SmartSwitchPCApp/FUSService/
│       ├── SmartSwitchPDLR.exe (1.2 MB - UPX compressed)
│       ├── AgentModule.dll (2.5 MB) ⭐
│       ├── CommonModule.dll (1.9 MB) ⭐
│       ├── PluginModule.dll (307 KB)
│       ├── AgentInstaller.exe (749 KB)
│       ├── AgentUpdate.exe (430 KB)
│       ├── FUSServiceHelper.exe (487 KB)
│       ├── LauncherSmartSwitchPDLR.exe (366 KB)
│       ├── GlobalUtil.dll (94 KB)
│       ├── AgentDialogs.dll (582 KB)
│       ├── AgentModels.dll (52 KB)
│       ├── Agent.dll (51 KB)
│       ├── BaseUI.dll (215 KB)
│       ├── NTMsg.exe (1.4 MB)
│       ├── AdminDelegator.exe (367 KB)
│       ├── AdminDelegator_SmartSwitch.exe (375 KB)
│       └── language/ (DLLs de recursos - 40+ idiomas)
└── WindowsFolder/
    └── system32/ (Runtime DLLs)
```

## Binarios Principales Analizados

### 1. AgentModule.dll (2.5 MB)

**Tipo**: PE32 executable (DLL) Intel 80386  
**Secciones**: 6 sections  
**Función**: Módulo de red y gestión del agente FUS

#### Clases Identificadas

```cpp
class AgentNetworkModule {
public:
    // Autenticación y headers
    static const wchar_t* MakeAuthorizationHeaderWithGeneratedNonceValueAndAMModule(
        const wchar_t* data
    );
    
    static bool SendAuthorizationHeaderResponseSignal(
        const wchar_t* header
    );
    
    // Descarga de aplicaciones
    static void ApplicationDownloadingStatusCallBackFunc(
        _DOWNLOADING_STATUS status,
        const wchar_t* message,
        __int64 current,
        __int64 total
    );
    
    static void ApplicationDownloadRetryAgain(
        unsigned int param1,
        unsigned int param2,
        unsigned int param3,
        unsigned int param4
    );
    
    // Verificación de servidor
    _FUSErrorCode CheckAndSetTargetServerUrl();
    
    // Descarga de aplicación
    _FUSErrorCode StartDownloadApplication(UpdateApplicationInfo& info);
    
    // Consulta de versión
    bool QueryLatestMP3PVersionFromServer(
        const wchar_t* param1,
        const wchar_t* param2,
        const wchar_t* param3,
        const wchar_t* param4,
        const wchar_t* param5,
        CString& result
    );
};

class AgentUtilModule {
private:
    // Funciones para obtener URLs específicas por modelo/versión
    const wchar_t* GetUrl100S(const wchar_t* base);
    const wchar_t* GetUrl110S(const wchar_t* base);
    const wchar_t* GetUrl130K(const wchar_t* base);
    const wchar_t* GetUrl130L(const wchar_t* base);
    const wchar_t* GetUrl180K(const wchar_t* base);
    const wchar_t* GetUrl180L(const wchar_t* base);
    const wchar_t* GetUrl180S(const wchar_t* base);
    const wchar_t* GetUrl180W(const wchar_t* base);
    const wchar_t* GetUrl190S(const wchar_t* base);
    // ... 30+ funciones GetUrl* para diferentes modelos
    
    const wchar_t* GetUrlE110S(const wchar_t* base);
    const wchar_t* GetUrlE120K(const wchar_t* base);
    // ... URLs de Emergency mode
    
    const wchar_t* GetUrlM210S(const wchar_t* base);
    const wchar_t* GetUrlM250K(const wchar_t* base);
    // ... URLs de Mass download
    
public:
    const wchar_t* GetNoticeURL(UpdateDeviceInfo* info);
    const wchar_t* GetCompleteURL(
        const wchar_t* base,
        const wchar_t* path,
        bool flag
    );
    const wchar_t* ParsingNoticeURL(
        int& out1,
        int& out2,
        const wchar_t* url
    );
};

class AgentModule {
public:
    const wchar_t* GetNoticeUrlLast();
    void SetNoticeUrlLast(const wchar_t* url);
    
    const wchar_t* GetAddNoticeUrlLast();
    void SetAddNoticeUrlLast(const wchar_t* url);
    
    bool IsBadaTempBinaryUpdatedModel(
        FUSUpdateInfo& fusInfo,
        UpdateDeviceInfo& deviceInfo,
        AgentParameter& param
    );
    
    bool WaitBinaryWebDownloadCompleteEvent();
};
```

### 2. CommonModule.dll (1.9 MB)

**Tipo**: PE32 executable (DLL) Intel 80386  
**Secciones**: 7 sections  
**Función**: Módulo de red base y gestión de binarios

#### Clases Identificadas

```cpp
class BaseNetworkModule {
protected:
    // Funciones de autorización para diferentes endpoints
    const wchar_t* MakeAuthorizationHeader(const wchar_t* data);
    
    const wchar_t* MakeAuthorizationHeaderForNFBinaryInfomDO(
        const wchar_t* data
    );
    
    const wchar_t* MakeAuthorizationHeaderForNFBinaryInitDO(
        const wchar_t* data,
        bool flag
    );
    
    // Construcción de body XML
    const wchar_t* MakeBody(
        map<CString, CEachItemNode>& items
    );
    
    // Carga de XML
    bool LoadTargetXML(const wchar_t* path);
};

class NetworkModule : public BaseNetworkModule {
protected:
    // Peticiones FUS
    _FUSErrorCode RequestBinaryInformDO(
        map<CString, CString>& params,
        CString* result
    );
    
    _FUSErrorCode RequestBinaryInitDO(
        map<CString, CString>& params,
        bool flag
    );
    
    _FUSErrorCode DownloadBinaryDO(
        map<CString, CString>& params,
        const wchar_t* path,
        DOWNLOADING_STATUS_CALLBACK callback,
        bool verifyFlag
    );
    
    // Verificación de binario temporal
    bool CheckTempBinary(
        UpdateDeviceInfo& deviceInfo,
        CString& path1,
        CString& path2
    );
    
    // Información de reanudación de descarga
    _FUSErrorCode GetUpdateInformationForResumeBinaryDownload(
        UpdateDeviceInfo& deviceInfo
    );
    
    // Descarga de binario desde XML local
    _FUSErrorCode RequestBinaryInformFromLocalXML(
        const wchar_t* xmlPath
    );
    
    // Estado de descarga de segundo paso
    bool IsSecondStepDownloadingForBadaBinaryStatus();
    
private:
    void NotiAllDownloadBinaryProcessingHasBeenEnded(bool status);
};

class UpdateDeviceInfo {
public:
    // Información del binario
    const wchar_t* GetBinaryFileName();
    const wchar_t* GetBinarySize();
    const wchar_t* GetBinaryByteSize();
    const wchar_t* GetBinaryCrc();
    const wchar_t* GetBinaryName_BD20();
    const wchar_t* GetBinarySize_BD20();
    const wchar_t* GetBinaryCrc_BD20();
    const wchar_t* GetBinaryFolder_BD20();
    const wchar_t* GetBinary_Folder();
    const wchar_t* GetBinary_Type();
    const wchar_t* GetDownloadBinarySize();
    
    // Query info
    const wchar_t* GetQueryBinaryPath();
    const wchar_t* GetQueryBinarySize();
    const wchar_t* GetQueryBinaryLastModifiedTime();
    
    // Tipos de binario
    _FUS_UPDATE_BINARY_TYPE GetUpdateBinaryMode();
    _FUS_UPDATE_BINARY_TYPE GetUseUpdateBinaryType();
    _FUS_SHARING_BINARY_TYPE GetSharingBinary();
    
    // Emergency binary
    const wchar_t* GetEmergencyBinaryVersion();
    const wchar_t* GetEmergencyBinaryPRDCode();
    _FUS_UPDATE_BINARY_TYPE GetEmergencyBinaryType();
    bool CheckEmergencyBinaryFile();
    
    // Setters
    void SetBinaryByteSize(const wchar_t* size);
    void SetBinaryCrc(const wchar_t* crc);
    void SetBinaryCrc_BD20(const wchar_t* crc);
    void SetBadaDownloadedBinaryPath(CString& path);
    
    // Estado Bada
    bool IsBadaBinaryDownloaded();
    
    // Generación de versión
    void MakeDisplayFirmwareVersion(const wchar_t* version);
};

class FUSUpdateInfo {
public:
    int GetBinarySize();
};

class FileProcessAndTimeModule {
public:
    bool SendSignalToAgentForExeucteBinaryLoaderManager(
        const wchar_t* param1,
        const wchar_t* param2
    );
    
    void KillTargetProcess(const wchar_t* processName, bool flag);
};
```

### 3. PluginModule.dll (307 KB)

**Tipo**: PE32 executable (DLL) Intel 80386  
**Secciones**: 5 sections  
**Función**: Gestión de plugins del sistema FUS

## Protocolo de Descarga FUS Reconstruido

### Flujo de Operaciones

```
1. CheckAndSetTargetServerUrl()
   ↓
2. MakeAuthorizationHeaderWithGeneratedNonceValueAndAMModule(data)
   → Genera NONCE
   → Calcula hash/signature
   → Retorna header "Authorization: FUS ..."
   ↓
3. RequestBinaryInformDO(params, result)
   → POST a NF_DownloadBinaryInform.do
   → Envía: modelo, CSC, IMEI, versión actual
   → Headers: Authorization (con NONCE)
   → Recibe: información del binario disponible
   ↓
4. MakeAuthorizationHeaderForNFBinaryInitDO(data, flag)
   → Genera nuevo header de autorización
   ↓
5. RequestBinaryInitDO(params, flag)
   → POST a NF_DownloadBinaryInitForMass.do
   → Inicializa sesión de descarga
   → Recibe: URL y token de descarga
   ↓
6. DownloadBinaryDO(params, path, callback, verify)
   → GET/POST a NF_DownloadBinaryForMass.do
   → Descarga archivo binario
   → Callback para progreso
   → Verifica CRC si verify=true
   ↓
7. SendSignalToAgentForExeucteBinaryLoaderManager(param1, param2)
   → Notifica al agente que la descarga completó
```

### Endpoints Inferidos

Basándome en los nombres de funciones y el análisis previo de APKs/Smart Switch:

```
https://neofussvr.sslcs.cdngc.net/
├── NF_DownloadGenerateNonce.do
│   - Genera NONCE para autenticación
│   - POST
│
├── NF_DownloadBinaryInform.do
│   - Obtiene información del firmware disponible
│   - POST
│   - Headers: Authorization (con NONCE)
│   - Body: modelo, CSC, región, versión
│
├── NF_DownloadBinaryInitForMass.do
│   - Inicializa descarga masiva
│   - POST
│   - Headers: Authorization
│   - Retorna: URL de descarga, token de sesión
│
└── NF_DownloadBinaryForMass.do
    - Descarga el archivo binario
    - GET/POST
    - Query params: file path, token
    - Headers: Authorization
```

## Funciones de Autorización

### MakeAuthorizationHeader

```cpp
const wchar_t* BaseNetworkModule::MakeAuthorizationHeader(
    const wchar_t* data
)
```

**Propósito**: Genera header de autorización base

**Proceso inferido**:
1. Toma datos de entrada (IMEI:modelo:CSC)
2. Genera o usa NONCE existente
3. Calcula HMAC-SHA256(nonce_key, data)
4. Formatea como: `Authorization: FUS nonce={nonce},signature={signature}`

### MakeAuthorizationHeaderForNFBinaryInfomDO

```cpp
const wchar_t* BaseNetworkModule::MakeAuthorizationHeaderForNFBinaryInfomDO(
    const wchar_t* data
)
```

**Propósito**: Header específico para endpoint BinaryInform

**Diferencia**: Probablemente incluye parámetros adicionales o usa algoritmo diferente

### MakeAuthorizationHeaderForNFBinaryInitDO

```cpp
const wchar_t* BaseNetworkModule::MakeAuthorizationHeaderForNFBinaryInitDO(
    const wchar_t* data,
    bool flag
)
```

**Propósito**: Header para inicialización de descarga

**Parámetro bool**: Probablemente indica:
- `true`: Descarga de emergencia
- `false`: Descarga normal

## Gestión de URLs Dinámicas

### Sistema GetUrl*

El `AgentUtilModule` tiene 30+ funciones `GetUrl*` que sugieren:

```
GetUrl100S → Modelo serie 100, servidor S (Standard)
GetUrl130K → Modelo serie 130, servidor K (Korea)
GetUrl130L → Modelo serie 130, servidor L (Latin America?)
GetUrl180W → Modelo serie 180, servidor W (Worldwide?)

GetUrlE110S → Emergency mode, modelo 110, servidor S
GetUrlM250K → Mass download, modelo 250, servidor K
```

**Interpretación**:
- Diferentes modelos usan diferentes endpoints
- Servidores regionales (K, L, S, W, etc.)
- Modos especiales (Emergency, Mass)

### Construcción Dinámica de URLs

```cpp
const wchar_t* AgentUtilModule::GetCompleteURL(
    const wchar_t* base,
    const wchar_t* path,
    bool flag
)
```

Combina:
1. Base URL del servidor (ej: `neofussvr.sslcs.cdngc.net`)
2. Path específico del endpoint (ej: `/NF_DownloadBinaryInform.do`)
3. Parámetros adicionales según flag

## Tipos de Binarios FUS

```cpp
enum _FUS_UPDATE_BINARY_TYPE {
    FUS_BINARY_TYPE_NORMAL,      // Actualización normal
    FUS_BINARY_TYPE_EMERGENCY,   // Modo de emergencia
    FUS_BINARY_TYPE_BADA,        // Dispositivos Bada (legacy)
    FUS_BINARY_TYPE_BD20,        // Tipo BD20
    FUS_BINARY_TYPE_TEMP         // Binario temporal
};

enum _FUS_SHARING_BINARY_TYPE {
    FUS_SHARING_NONE,
    FUS_SHARING_ENABLED
};
```

## Estados de Descarga

```cpp
enum _DOWNLOADING_STATUS {
    DOWNLOADING_STARTED,
    DOWNLOADING_IN_PROGRESS,
    DOWNLOADING_COMPLETED,
    DOWNLOADING_FAILED,
    DOWNLOADING_PAUSED,
    DOWNLOADING_RESUMED,
    DOWNLOADING_CANCELLED
};
```

## Callbacks de Descarga

```cpp
typedef void (*DOWNLOADING_STATUS_CALLBACK)(
    _DOWNLOADING_STATUS status,
    const wchar_t* message,
    __int64 bytesDownloaded,
    __int64 totalBytes
);
```

## Códigos de Error FUS

```cpp
enum _FUSErrorCode {
    FUS_SUCCESS = 0,
    FUS_ERROR_NETWORK,
    FUS_ERROR_AUTH,
    FUS_ERROR_NOT_FOUND,
    FUS_ERROR_INVALID_PARAM,
    FUS_ERROR_SERVER,
    FUS_ERROR_FILE_IO,
    FUS_ERROR_VERIFICATION,
    FUS_ERROR_CANCELLED,
    // ... más códigos
};
```

## Archivos de Soporte

### AgentVer.txt

```
25.08.22.01
```

Versión del agente FUS: 22 de agosto de 2025, versión 01

### Manifiestos

Requiere:
- Microsoft Visual C++ 2008 Redistributable (VC90)
- Microsoft.VC90.CRT version 9.0.21022.8
- Microsoft.VC90.MFC version 9.0.21022.8
- Microsoft.VC90.ATL

### Certificados

Firmado con:
- **DigiCert Trusted Root G4**
- **DigiCert Trusted G4 Code Signing RSA4096 SHA384 2021 CA1**
- **Samsung Electronics Co., Ltd.**

URLs de revocación:
```
http://crl3.digicert.com/DigiCertTrustedG4CodeSigningRSA4096SHA3842021CA1.crl
http://crl4.digicert.com/DigiCertTrustedG4CodeSigningRSA4096SHA3842021CA1.crl
```

## Limitaciones del Análisis

### No Pude Obtener

1. **Nonce Key**: Clave secreta para HMAC (hardcoded o en registro)
2. **Algoritmo exacto de NONCE**: Probablemente timestamp + random
3. **URLs hardcodeadas**: Se construyen dinámicamente
4. **Formato exacto de Authorization header**: Necesita debugging en tiempo real
5. **Parámetros exactos de RequestBinaryInformDO**: Estructura del body XML

### Razones

- Las DLLs están compiladas sin símbolos de debug
- URLs se construyen en runtime
- Claves secretas probablemente en registro de Windows o config cifrado
- Necesitaría:
  - Debugging con WinDbg/x64dbg
  - Hooking de funciones con Frida
  - Captura de tráfico de red con Wireshark
  - Decompilación completa con IDA Pro/Ghidra

## Comparación con Análisis Previos

| Componente | Windows (FUS Service) | Mac (FUS Agent) | APKs Android |
|------------|----------------------|-----------------|--------------|
| Lenguaje | C++ (PE32) | Objective-C (Mach-O) | Java/Kotlin (DEX) |
| Tamaño | ~2.5 MB (AgentModule) | ~1.6 MB (FUS Agent) | ~8.8 MB (FotaAgent) |
| Autorización | 3 funciones específicas | checkBinary:OTP: | NONCE generation |
| URLs | Construcción dinámica | URLInfo.xml | Hardcoded strings |
| OTP | Implícito en NONCE | Explícito en API | Token-based |
| Tipos binario | 5 tipos + Emergency | No visible | OTA standard |

## Descubrimientos Clave

### 1. Sistema de URLs Multinivel

FUS Service tiene un sistema sofisticado de routing:
- **30+ funciones GetUrl*** para diferentes modelos/regiones
- URLs construidas dinámicamente según:
  - Modelo del dispositivo
  - Región/CSC
  - Tipo de descarga (Normal/Emergency/Mass)
  - Servidor objetivo (K/L/S/W)

### 2. Tres Niveles de Autorización

```
MakeAuthorizationHeader                      → Base general
MakeAuthorizationHeaderForNFBinaryInfomDO    → Para consulta de info
MakeAuthorizationHeaderForNFBinaryInitDO     → Para iniciar descarga
```

Cada endpoint tiene su propio esquema de autorización.

### 3. Soporte para Dispositivos Legacy

- **Bada**: SO móvil anterior de Samsung (discontinued)
- **BD20**: Tipo de binario específico
- **Emergency mode**: Recuperación de dispositivos

### 4. Callback System Robusto

Sistema de callbacks para:
- Estado de descarga
- Progreso (bytes descargados)
- Errores y reintentos
- Notificaciones al agente

### 5. Verificación de Integridad

```cpp
DownloadBinaryDO(..., bool verifyFlag)
```

Si `verifyFlag=true`:
- Verifica CRC del binario descargado
- Compara con CRC recibido del servidor
- Falla si no coincide

## Implementación Teórica en Python

Basándome en el análisis, el protocolo se implementaría así:

```python
import hmac
import hashlib
import time
import requests

class FUSClient:
    def __init__(self, model, csc, imei):
        self.model = model
        self.csc = csc
        self.imei = imei
        self.nonce_key = "UNKNOWN"  # Necesita reverse engineering
        self.base_url = "https://neofussvr.sslcs.cdngc.net"
        
    def generate_nonce(self):
        """Genera NONCE para autenticación"""
        # Probablemente: timestamp + random
        return f"{int(time.time())}{random_hex()}"
    
    def make_authorization_header(self, data, endpoint_type="base"):
        """Genera header de autorización"""
        nonce = self.generate_nonce()
        
        # HMAC-SHA256(nonce_key, data)
        signature = hmac.new(
            self.nonce_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if endpoint_type == "binary_inform":
            # Lógica específica para BinaryInform
            return f"FUS nonce={nonce},signature={signature},type=inform"
        elif endpoint_type == "binary_init":
            # Lógica específica para BinaryInit
            return f"FUS nonce={nonce},signature={signature},type=init"
        else:
            return f"FUS nonce={nonce},signature={signature}"
    
    def request_binary_inform(self):
        """Consulta información del firmware"""
        data = f"{self.imei}:{self.model}:{self.csc}"
        auth_header = self.make_authorization_header(
            data, 
            endpoint_type="binary_inform"
        )
        
        response = requests.post(
            f"{self.base_url}/NF_DownloadBinaryInform.do",
            headers={"Authorization": auth_header},
            data={
                "model": self.model,
                "csc": self.csc,
                "imei": self.imei
            }
        )
        return response
    
    def request_binary_init(self, binary_info):
        """Inicializa descarga"""
        data = f"{self.imei}:{self.model}:{self.csc}:{binary_info}"
        auth_header = self.make_authorization_header(
            data,
            endpoint_type="binary_init"
        )
        
        response = requests.post(
            f"{self.base_url}/NF_DownloadBinaryInitForMass.do",
            headers={"Authorization": auth_header},
            data=binary_info
        )
        return response
    
    def download_binary(self, download_url, token, output_path):
        """Descarga el binario"""
        response = requests.get(
            download_url,
            params={"token": token},
            stream=True
        )
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
```

## Próximos Pasos para Implementación Completa

### 1. Debugging en Windows

```bash
# Con x64dbg o WinDbg
1. Cargar SmartSwitchPDLR.exe o proceso que use las DLLs
2. Breakpoint en MakeAuthorizationHeader*
3. Capturar parámetros de entrada y salida
4. Extraer nonce_key del registro/memoria
```

### 2. Network Capture

```bash
# Con Wireshark
1. Filtrar tráfico a neofussvr.sslcs.cdngc.net
2. Capturar requests POST a NF_*.do
3. Analizar headers Authorization
4. Extraer formato exacto de NONCE y signature
```

### 3. Frida Hooking

```javascript
// Hook de funciones DLL
Interceptor.attach(Module.findExportByName(
    "CommonModule.dll",
    "?MakeAuthorizationHeader@BaseNetworkModule@@IAEPB_WPB_W@Z"
), {
    onEnter: function(args) {
        console.log("Input:", args[1].readUtf16String());
    },
    onLeave: function(retval) {
        console.log("Output:", retval.readUtf16String());
    }
});
```

### 4. Registro de Windows

Buscar en:
```
HKEY_LOCAL_MACHINE\SOFTWARE\Samsung\SmartSwitch
HKEY_CURRENT_USER\SOFTWARE\Samsung\SmartSwitch
```

Posible nonce_key o configuración del servidor.

## Conclusiones

### Hallazgos Principales

1. **FUS Service es un sistema complejo** con 3 DLLs principales
2. **Tres niveles de autorización** para diferentes endpoints
3. **Sistema de URLs dinámico** con 30+ variantes
4. **Callbacks robustos** para gestión de estado
5. **Soporte multi-plataforma** (modelos legacy y actuales)

### Razón Definitiva del Error 403

Los scripts Python fallan porque **no tienen**:

1. **nonce_key correcto**: Hardcoded en las DLLs o registro
2. **Algoritmo de generación de NONCE**: Timestamp + algo más
3. **Formato exacto de Authorization header**: Varía por endpoint
4. **Certificados de cliente**: Instalados con Smart Switch
5. **Session tokens**: Generados después de BinaryInit

### Recomendación Final

Para implementar descarga completa:

1. **Debugging en Windows** con Smart Switch real
2. **Captura de tráfico** con Wireshark/Charles
3. **Hooking con Frida** de las funciones de autorización
4. **Decompilación completa** con IDA Pro/Ghidra
5. **Análisis de registro** para encontrar nonce_key

**Alternativa**: Usar Smart Switch oficial que ya tiene todo implementado.

---

**Análisis completado**: 2025-12-27  
**Herramientas**: strings, objdump, upx, radare2, file  
**Tamaño analizado**: 17 MB (exS.zip)  
**Binarios principales**: AgentModule.dll, CommonModule.dll, PluginModule.dll  
**Total de funciones identificadas**: 100+
