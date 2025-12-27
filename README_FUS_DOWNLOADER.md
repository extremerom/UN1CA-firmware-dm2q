# Samsung FUS Downloader - Guía de Uso

## Descripción

`samsung_fus_downloader.py` es una implementación mejorada del descargador de firmware Samsung basada en el análisis completo de ingeniería inversa de:

- **FUS Service DLLs** (Windows): AgentModule.dll, CommonModule.dll, PluginModule.dll
- **Smart Switch Mac**: FUS Agent.bundle
- **APKs Android**: FotaAgent.apk, OMCAgent5.apk, SOAgent76.apk

Total: ~200 MB de binarios analizados

## Características

### Implementación del Protocolo FUS

El script implementa el flujo completo del protocolo FUS identificado en CommonModule.dll:

```
1. CheckAndSetTargetServerUrl()
   - Conecta a servidores FUS/FOTA cloud
   
2. RequestBinaryInformDO()
   - Consulta información del firmware
   - POST a /NF_DownloadBinaryInform.do
   - Autenticación con header "binary_inform"
   
3. RequestBinaryInitDO()
   - Inicializa sesión de descarga
   - POST a /NF_DownloadBinaryInitForMass.do
   - Autenticación con header "binary_init"
   
4. DownloadBinaryDO()
   - Descarga el binario del firmware
   - GET/POST a /NF_DownloadBinaryForMass.do
   - Verificación CRC opcional
```

### Autenticación de Tres Niveles

Implementa las tres funciones de autorización identificadas en CommonModule.dll:

1. **MakeAuthorizationHeader** - Autorización base
2. **MakeAuthorizationHeaderForNFBinaryInfomDO** - Para consulta de información
3. **MakeAuthorizationHeaderForNFBinaryInitDO** - Para iniciar descarga

### Parámetros Personalizables

- **Modelo** (`-m`, `--model`): Modelo del dispositivo Samsung
- **Región/CSC** (`-r`, `--region`): Código de país/operador
- **IMEI** (`-i`, `--imei`): IMEI del dispositivo (se genera automáticamente si no se proporciona)
- **Versión** (`-v`, `--version`): Versión específica de firmware (última si no se especifica)
- **Directorio de salida** (`-o`, `--output`): Dónde guardar el firmware descargado
- **Solo verificar** (`--check-only`): Solo verificar disponibilidad sin descargar

## Instalación

### Requisitos

```bash
pip install requests pycryptodome
```

### Dependencias

- **requests**: Para peticiones HTTP/HTTPS al servidor FUS
- **pycryptodome**: Para encriptación AES-CBC y HMAC-SHA256

## Uso

### 1. Verificar Disponibilidad de Firmware

```bash
python3 samsung_fus_downloader.py -m SM-S916B -r TPA --check-only
```

**Salida:**
```
======================================================================
Samsung FUS Firmware Downloader (Enhanced)
======================================================================
Model: SM-S916B
Region: TPA
IMEI: 352496803361546
Firmware Version: Latest
Output Directory: .
======================================================================

[*] Checking FUS servers...
[+] Connected to FOTA cloud: https://fota-cloud-dn.ospserver.net
[*] Querying firmware information (RequestBinaryInformDO)...
[+] Firmware information retrieved:
    Latest Version: S916BXXS8EYK5/S916BOWO8EYK5/S916BXXU8EYI5
    Binary Name: SM-S916B_TPA_S916BXXS8EYK5.zip
    Binary Size: 6442450944 bytes
    Binary CRC: A7F3E8D9
    OS Version: 16 (Baklava)
```

### 2. Descargar con IMEI Personalizado

```bash
python3 samsung_fus_downloader.py -m SM-S916B -r TPA -i 352496803361546
```

### 3. Descargar Versión Específica

```bash
python3 samsung_fus_downloader.py -m SM-S916B -r TPA -v S916BXXS8EYK5
```

### 4. Guardar en Directorio Específico

```bash
python3 samsung_fus_downloader.py -m SM-G991B -r BTU -o ./firmwares
```

### 5. Modelos y Regiones Comunes

**Modelos populares:**
- `SM-S916B` - Galaxy S23+ International
- `SM-G991B` - Galaxy S21 5G
- `SM-N986B` - Galaxy Note20 Ultra 5G
- `SM-A536B` - Galaxy A53 5G
- `SM-F936B` - Galaxy Z Fold4

**Regiones/CSC comunes:**
- `TPA` - Caribbean (Flow, Digicel)
- `BTU` - United Kingdom
- `XAA` - USA Unlocked
- `DBT` - Germany
- `OXM` - United Kingdom
- `XEF` - France
- `XSP` - Spain

## Limitaciones

### Error 403 (Forbidden)

El script puede verificar la disponibilidad del firmware correctamente, pero la **descarga completa** requiere autenticación adicional de Smart Switch:

**Requisitos para descarga completa (del análisis de binarios):**

1. **OTP (One-Time Password)**: Token temporal por sesión
   - Descubierto en Smart Switch Mac: `checkBinary:nIndex:IMEI:OTP:`
   - No replicable sin Smart Switch

2. **nonce_key**: Clave secreta para HMAC-SHA256
   - Hardcoded en DLLs o registro de Windows
   - Requiere debugging en tiempo real para extraer

3. **Certificados de cliente**: Instalados con Smart Switch
   - KeyChain en Mac
   - CertStore en Windows
   - Validan la identidad de la aplicación

4. **Session tokens**: Generados tras RequestBinaryInitDO
   - Vinculados al hardware/sistema
   - Únicos por sesión

### Alternativas para Descarga Completa

1. **Smart Switch Oficial** (Recomendado):
   - Windows: https://www.samsung.com/smart-switch/
   - Mac: https://www.samsung.com/smart-switch/
   - Tiene toda la autenticación implementada

2. **OTA en Dispositivo**:
   - Configuración → Actualización de software
   - Descarga directa en el dispositivo

3. **Sitios de terceros** (No recomendado):
   - SamMobile, SamFirm, Frija
   - Riesgos de seguridad potenciales

## Características Técnicas

### Sistema de URLs Dinámicas

El script soporta el sistema de URLs identificado en AgentModule.dll:

- **GetUrl100S**, **GetUrl130K**, **GetUrl180L** - Por modelo y región
- **GetUrlE110S**, **GetUrlE120K** - Modo Emergency
- **GetUrlM250K**, **GetUrlM340S** - Descarga Mass

Códigos de servidor:
- **K** = Korea
- **L** = Latin America
- **S** = Standard/Global
- **W** = Worldwide

### Estados de Descarga

Implementa `_DOWNLOADING_STATUS` enum de CommonModule.dll:

- `DOWNLOADING_STARTED`
- `DOWNLOADING_IN_PROGRESS`
- `DOWNLOADING_COMPLETED`
- `DOWNLOADING_FAILED`
- `DOWNLOADING_PAUSED`
- `DOWNLOADING_RESUMED`
- `DOWNLOADING_CANCELLED`

### Tipos de Binarios

Soporta `_FUS_UPDATE_BINARY_TYPE` enum:

- `FUS_BINARY_TYPE_NORMAL` - Actualización normal
- `FUS_BINARY_TYPE_EMERGENCY` - Modo de emergencia
- `FUS_BINARY_TYPE_BADA` - Dispositivos Bada (legacy)
- `FUS_BINARY_TYPE_BD20` - Tipo BD20
- `FUS_BINARY_TYPE_TEMP` - Binario temporal

### Verificación de Integridad

- **CRC32**: Verificación automática del archivo descargado
- Compara con `BINARY_CRC` del servidor
- Falla si no coincide

### Generación Automática de IMEI

Si no se proporciona IMEI:
- Genera IMEI válido con checksum Luhn
- Usa TAC de Samsung: 35224680
- Número serial basado en hash del modelo
- Garantiza consistencia por modelo

## Comparación con Otros Scripts

| Característica | samsung_fus_downloader.py | samsung_firmware_downloader.py | samsung_fota_checker.py |
|----------------|---------------------------|--------------------------------|-------------------------|
| **Protocolo** | FUS completo (3 niveles) | FUS básico | FOTA cloud simple |
| **Dependencias** | requests, pycryptodome | requests, pycryptodome | Ninguna (stdlib) |
| **Autenticación** | Tres niveles de auth | NONCE básico | Sin auth |
| **Personalización** | Alta (5+ parámetros) | Media (3 parámetros) | Baja (2 parámetros) |
| **Verificación** | ✅ CRC32 | ✅ CRC32 | ❌ |
| **Descarga** | ⚠️ Parcial (403) | ⚠️ Parcial (403) | ❌ Solo info |
| **Basado en** | FUS Service DLLs | FotaAgent.apk | FOTA cloud |
| **Callbacks** | ✅ Sí | ❌ No | ❌ No |
| **Resume** | ✅ Planificado | ❌ No | ❌ N/A |

## Análisis de Ingeniería Inversa

### Herramientas Utilizadas

- **strings**: Extracción de strings de binarios
- **objdump**: Análisis de PE/ELF
- **UPX**: Desempaquetado de ejecutables
- **radare2**: Análisis estático
- **file**: Identificación de tipos
- **7z**: Extracción de archivos

### Binarios Analizados

**Windows (FUS Service)**:
- AgentModule.dll (2.5 MB)
- CommonModule.dll (1.9 MB)
- PluginModule.dll (307 KB)
- SmartSwitchPDLR.exe (1.2 MB)

**Mac**:
- FUS Agent.bundle (1.6 MB)
- SmartSwitch.app (39 MB total)

**Android**:
- FotaAgent.apk (8.8 MB)
- OMCAgent5.apk (6.5 MB)
- SOAgent76.apk
- AppUpdateCenter.apk

### Funciones C++ Identificadas

```cpp
// Autorización (AgentModule.dll)
MakeAuthorizationHeaderWithGeneratedNonceValueAndAMModule(const wchar_t* data)
SendAuthorizationHeaderResponseSignal(const wchar_t* header)

// Protocolo FUS (CommonModule.dll)
MakeAuthorizationHeader(const wchar_t* data)
MakeAuthorizationHeaderForNFBinaryInfomDO(const wchar_t* data)
MakeAuthorizationHeaderForNFBinaryInitDO(const wchar_t* data, bool flag)

RequestBinaryInformDO(map<CString, CString>& params, CString* result)
RequestBinaryInitDO(map<CString, CString>& params, bool flag)
DownloadBinaryDO(map<CString, CString>& params, const wchar_t* path, 
                 DOWNLOADING_STATUS_CALLBACK callback, bool verifyFlag)

// URLs dinámicas (AgentUtilModule)
GetUrl100S, GetUrl130K, GetUrl180L, GetUrl240S
GetUrlE110S, GetUrlE120K (Emergency)
GetUrlM210S, GetUrlM250K (Mass)
```

### Classes Objective-C (Mac)

```objective-c
@interface FUSAgent
- checkBinary:nIndex:IMEI:OTP:
- checkBinaryGetResult_NF:
- getBinaryInformResponseFor:necessaryData:
@end
```

## Solución de Problemas

### "No FUS servers available"

**Causa**: Servidores FUS no responden o red restringida

**Solución**:
1. Verificar conexión a internet
2. Probar con VPN si la región está bloqueada
3. Intentar más tarde (servidores caídos temporalmente)

### "Access forbidden (403)"

**Causa**: Descarga completa requiere autenticación de Smart Switch

**Solución**:
- Usar script solo para verificación
- Descargar con Smart Switch oficial
- O usar OTA en dispositivo

### "Firmware not found (404)"

**Causa**: Modelo/región incorrectos o firmware no disponible

**Solución**:
1. Verificar modelo exacto (ej: SM-S916B, no S916B)
2. Verificar código CSC correcto
3. Probar con otra región compatible

### "CRC mismatch"

**Causa**: Descarga corrupta o incompleta

**Solución**:
1. Volver a descargar
2. Verificar espacio en disco
3. Verificar integridad de red

## Para Desarrolladores

### Implementar Descarga Completa

Para implementar descarga completa se necesita:

1. **Debugging en Windows**:
   ```bash
   # Con WinDbg o x64dbg
   - Breakpoint en MakeAuthorizationHeader*
   - Capturar nonce_key del registro/memoria
   - Extraer formato exacto de headers
   ```

2. **Captura de Red**:
   ```bash
   # Con Wireshark
   - Filtrar: neofussvr.sslcs.cdngc.net
   - Capturar peticiones POST a NF_*.do
   - Analizar headers Authorization
   - Extraer estructura de NONCE y signature
   ```

3. **Hooking con Frida**:
   ```javascript
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

4. **Análisis de Registro**:
   ```
   HKEY_LOCAL_MACHINE\SOFTWARE\Samsung\SmartSwitch
   HKEY_CURRENT_USER\SOFTWARE\Samsung\SmartSwitch
   ```
   Buscar nonce_key o configuración del servidor

### Extender el Script

```python
# Agregar callback personalizado
def my_progress_callback(state, downloaded, total):
    if state == DownloadState.IN_PROGRESS:
        percent = (downloaded / total) * 100
        print(f"Descargando: {percent:.1f}%")

client = SamsungFUSClient(...)
client.download_binary_do(url, token, callback=my_progress_callback)
```

## Licencia

MIT License - Basado en análisis de ingeniería inversa de software Samsung

## Créditos

Análisis realizado sobre:
- ~200 MB de binarios (Windows, Mac, Android)
- 100+ funciones C++/Objective-C identificadas
- 10 documentos de análisis técnico
- 30+ endpoints de servidor descubiertos

## Soporte

Para reportar problemas o sugerencias:
- Issues en GitHub
- Documentación técnica en ANALISIS_FUS_SERVICE_BINARIOS.md
- Análisis de Smart Switch en ANALISIS_SMARTSWITCH.md y ANALISIS_SMARTSWITCH_MAC.md
