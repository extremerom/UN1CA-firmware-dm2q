# Análisis de Smart Switch para Mac

## Información de la Aplicación

**Versión**: Descargada 2024-09-10  
**Tamaño**: 39 MB (40,275,181 bytes)  
**Tipo**: DMG → PKG → .app Bundle  
**Arquitectura**: Universal Binary (x86_64 + ARM64)  

## Estructura del Paquete

```
SmartSwitch4Mac.dmg
└── SmartSwitch.app/
    └── Contents/
        ├── MacOS/
        │   ├── SmartSwitch (14.6 MB - Binario principal)
        │   ├── KMBase.framework
        │   ├── Smart Switch Update.app
        │   └── ...
        ├── Frameworks/
        │   └── DeviceCenter.framework (Comunicación con dispositivo)
        ├── Resources/
        │   ├── SAMSUNG FUS Agent.bundle/ ⭐
        │   │   └── Contents/MacOS/
        │   │       └── SAMSUNG FUS Agent (1.6 MB)
        │   └── ... (NIBs, imágenes, etc.)
        └── Info.plist
```

## FUS Agent Encontrado

### Ubicación
`SmartSwitch.app/Contents/Resources/SAMSUNG FUS Agent.bundle/`

### Binario Principal
**Archivo**: `SAMSUNG FUS Agent` (1.6 MB)  
**Tipo**: Mach-O Universal Binary (x86_64 + ARM64)

### Clases Identificadas

```objective-c
@interface FUSAgent : NSObject
// Métodos principales
- (void)checkBinary:(id)arg1 nIndex:(int)arg2 IMEI:(NSString*)imei OTP:(id)otp;
- (void)checkBinaryForInit:(id)arg1 nIndex:(int)arg2 IMEI:(NSString*)imei OTP:(id)otp;
- (void)checkBinaryGetResult_NF:(id)userText;
- (void)getBinaryInformResponseFor:(id)arg1 necessaryData:(id)arg2;
+ (long long)getBinarySize;
- (void)setBinaryNatureInfoForInit:(id)arg1;
@end
```

### Funciones de Red

```
- URLInfoDic (Diccionario con información de servidores)
- getURLInfoDicForInit
- getPrivacyPolicyUrl
- TARGET_SERVER
- STAGING_SERVER_FLAG
- FIXED_TEST_SERVER_URL
```

## Servidores Identificados

### Principal
```
neofussvr.sslcs.cdngc.net
```

### URLs Encontradas

1. **Política de Privacidad FUS**:
   ```
   https://neofussvr.sslcs.cdngc.net/pp_SmartSwitch.htm
   ```

2. **Crash Report**:
   ```
   https://ccr.sec-smartswitch.com/upload_pc/
   ```

3. **Actualizaciones y Ayuda**:
   ```
   https://update.kies.samsung.com/SmartSwitchPC_mac_connect/mac/connection/?lang=%@&index=2
   https://update.kies.samsung.com/update/smartswitch_mac/help?lang=%@
   https://update.kies.samsung.com/update/smartswitch_mac/notice?region=%@&isTest=false
   https://update.kies.samsung.com/update/smartswitch_mac/notice?region=%@&isTest=true
   ```

4. **VAS (Value Added Service - Apps)**:
   ```
   https://vas.samsungapps.com/stub/stubDownload.as?appId=com.sec.android.easyMover&callerId=SSPC&stduk=%s&deviceId=%s&mcc=450&mnc=05&csc=%s&sdkVer=%d&isAutoUpdate=0&pd=%d
   https://vas.samsungapps.com/stub/stubUpdateCheck.as?appId=com.sec.android.easyMover&callerId=SSPC&versionCode=1&deviceId=%s&mcc=450&mnc=05&csc=%s&sdkVer=%d&pd=%d
   ```

5. **Imágenes de Modelos**:
   ```
   https://update.kies.samsung.com/update/smartswitchpc/image?model=%@&ProductCode=%@
   https://update.kies.samsung.com/update/smartswitchpc/image?model=apkfile
   ```

## Configuración de Servidor (URLInfo.xml)

El FUS Agent usa un archivo XML llamado `URLInfo.xml` que contiene:

```xml
<FUSMsg>
  <FUSBody>
    <Put>
      <CASH_SERVER_IP><Data>...</Data></CASH_SERVER_IP>
      <NOTICE_URL_FIRST><Data>...</Data></NOTICE_URL_FIRST>
      <NOTICE_URL_LAST><Data>...</Data></NOTICE_URL_LAST>
      <ADD_NOTICE_URL_FIRST><Data>...</Data></ADD_NOTICE_URL_FIRST>
      <ADD_NOTICE_URL_LAST><Data>...</Data></ADD_NOTICE_URL_LAST>
      <TARGET_SERVER><Data>...</Data></TARGET_SERVER>
    </Put>
  </FUSBody>
</FUSMsg>
```

**Nota**: Este archivo probablemente se descarga dinámicamente del servidor FUS.

## Protocolo de Descarga FUS (Mac)

### Flujo Identificado

```
1. Inicialización
   - Cargar URLInfoDic desde servidor
   - Verificar TARGET_SERVER vs STAGING_SERVER
   
2. Verificación de Binario (checkBinary/checkBinaryForInit)
   - Parámetros: nIndex, IMEI, OTP
   - Llamada: checkBinaryGetResult_NF
   - Response: getBinaryInformResponseFor:necessaryData:
   
3. Obtener información del binario
   - getBinarySize
   - setBinaryNatureInfoForInit
   
4. Descarga
   - needToUpgradeBinary = YES
   - FirmwareUpgradeNotificaton enviado
   - Descarga desde servidor FUS
```

### Parámetros Requeridos

- **IMEI**: Identificador del dispositivo
- **OTP**: One-Time Password (posiblemente token temporal)
- **nIndex**: Índice de binario/firmware
- **Model**: Modelo del dispositivo
- **CSC**: Código regional

## Comparación: Mac vs Windows

| Característica | Windows (MSIX) | Mac (DMG) |
|----------------|----------------|-----------|
| Lenguaje principal | C# (.NET 6) | Objective-C |
| FUS Component | SmartSwitchApp.Core.dll | SAMSUNG FUS Agent.bundle |
| Arquitectura | WinUI 3 + C++ DLLs | Cocoa + Frameworks nativos |
| Tamaño | 114 MB | 39 MB |
| Binario FUS | DLLs nativas C++ | Mach-O universal binary |
| URL Config | Hardcoded en DLLs | URLInfo.xml dinámico |

### Similitudes

1. **Servidor FUS**: Ambos usan `neofussvr.sslcs.cdngc.net`
2. **Protocolo XML**: Formato `<FUSMsg><FUSBody><Put>` en ambos
3. **Verificación Binaria**: Ambos hacen `checkBinary` antes de descargar
4. **Autenticación**: Ambos requieren IMEI/token

### Diferencias Clave

1. **Mac usa URLInfo.xml dinámico** (se descarga del servidor)
2. **Windows tiene URLs hardcodeadas** en las DLLs
3. **Mac parece más flexible** con servidores de staging/testing

## Frameworks de Comunicación

### DeviceCenter.framework

Maneja comunicación con el dispositivo Samsung:

```
- SamsungMTPSdk.framework (MTP protocol)
- SamsungMTPSdkCore.framework
- ssudAoaSdk.framework (AOA - Android Open Accessory)
- ssudmtpsdk.framework
- ssudmtpcore.framework
- KMBase.framework
- vObjectEncoding.framework
```

## Métodos de Backup/Restore

Identificados en el binario principal:

```objective-c
// Backup
- (void)setupFUS:
- (void)startFUSBackup
- (void)FUSStartBackup
- (void)BNRforFUSDoneWithStatus:BNRStatus:

// FUS Mode
- (void)enterFUSMode:
- (BOOL)isFUSOnly:
- (void)FUSUpgradeFirmware:
- (void)setupFUSState:

// Device Info
- (void)getDeviceInfoFUS:
- (void)DeviceFUSInfoWithLocationID:
- (void)updateFUSInfo:

// Notifications
- (void)FUSDeviceCheckNotificaton:
- (void)FUSDoneNotification:
- (void)FUSObexCommandNotification:
- (void)EnterFUSModeNotification:
```

## Descubrimientos Importantes

### 1. OTP (One-Time Password)

El FUS Agent usa un parámetro `OTP` en `checkBinary:nIndex:IMEI:OTP:`. Esto sugiere que:

- Se genera un token temporal por sesión
- Este token se usa para autenticar la descarga
- Explica por qué los scripts Python obtienen 403

### 2. URLInfo.xml Dinámico

A diferencia de Windows, Mac descarga la configuración del servidor dinámicamente:

```
"use stg svr. skip to set new urlinfo"
"use fixed test server. set value of FIXED_TEST_SERVER_URL"
"[CheckLocalPlugin] ServerVersion is Latest"
```

Esto significa que el servidor FUS puede:
- Cambiar endpoints sin actualizar la app
- Redirigir a servidores de staging para testing
- Actualizar plugins remotamente

### 3. Flags de Configuración

```
STAGING_SERVER_FLAG - Usar servidor de staging
FIXED_TEST_SERVER_URL - URL de servidor fijo para testing
FUS_SNCD_IP/TARGET_SERVER - Servidor objetivo
```

## Plugins y Componentes

### FUS Agent Sub-componentes

```
SAMSUNG FUS Agent.bundle/Contents/Resources/
├── fuspredownloader.app (Pre-descargador)
├── PreDownloadNotify.app (Notificaciones)
├── S1PlugIn.bundle (Plugin S1)
└── Comm.bundle (Comunicación)
```

### Sistema de Plugins

```
"launchPlugin URLInfoDic=%@"
"[CheckLocalPlugin] LocalVersion : %@ / ServerVersion : %@"
"[CheckLocalPlugin] ServerVersion is Latest. LocalVersion should Delete."
```

El FUS Agent tiene un sistema de plugins que:
- Se actualizan automáticamente desde el servidor
- Se verifican versiones local vs servidor
- Se eliminan versiones antiguas automáticamente

## Proceso de Descarga (Reconstruido)

Basado en el análisis, el proceso completo sería:

```python
# 1. Obtener URLInfo.xml del servidor FUS
urlinfo = download_from_fus("URLInfo.xml")

# 2. Parsear TARGET_SERVER
target_server = parse_xml(urlinfo, "TARGET_SERVER")

# 3. Generar OTP (One-Time Password)
otp = generate_otp_token()  # Método desconocido

# 4. Verificar binario disponible
response = check_binary(
    server=target_server,
    nIndex=0,
    imei=device_imei,
    otp=otp
)

# 5. Si needToUpgradeBinary == YES
if response.needToUpgradeBinary:
    binary_info = get_binary_inform(
        response.necessaryData
    )
    
    # 6. Descargar firmware
    firmware_data = download_firmware(
        server=target_server,
        binary_info=binary_info,
        otp=otp
    )
```

## Limitaciones del Análisis

### No Pude Determinar

1. **Algoritmo de generación de OTP**: Probablemente basado en:
   - Timestamp
   - IMEI
   - Secret key (hardcoded o desde KeyChain)

2. **Formato exacto de checkBinary request**: Necesitaría:
   - Decompilación completa del binario Mach-O
   - Análisis de tráfico de red real
   - Debugging de la aplicación en ejecución

3. **Estructura de URLInfo.xml**: No está incluido en el bundle, se descarga dinámicamente

## Conclusiones

### Diferencias Clave vs Windows

1. **Mac es más flexible**: Configuración dinámica de servidores
2. **Autenticación OTP**: Mac usa OTP explícitamente
3. **Sistema de plugins**: Mac puede actualizar componentes sin reinstalar
4. **Servidores de testing**: Mac tiene soporte para staging built-in

### Por qué el Script Python falla (403)

El script Python no tiene:

1. **OTP válido**: No sabemos cómo generarlo
2. **URLInfo.xml**: No tenemos acceso a la config del servidor
3. **Autenticación de app**: Smart Switch se identifica de forma única
4. **Certificados**: Probablemente usa certificados del KeyChain en Mac

### Recomendaciones

Para implementar descarga completa:

1. **Captura de tráfico**: Usar Wireshark/Charles Proxy con Smart Switch
2. **Decompilación**: Usar Hopper/IDA Pro en el binario Mach-O
3. **Debugging**: Instrumentar con lldb/dtrace
4. **Análisis de KeyChain**: Ver si hay certificados almacenados

## Archivos del Análisis

```
/tmp/smartswitch_mac/
└── SmartSwitch/
    └── pkg_extracted/
        └── app/
            ├── SmartSwitch.app/ (Aplicación principal)
            │   ├── Contents/MacOS/SmartSwitch (14.6 MB)
            │   ├── Contents/Frameworks/DeviceCenter.framework
            │   └── Contents/Resources/SAMSUNG FUS Agent.bundle/ (1.6 MB)
            └── Uninstall.app/
```

## Referencias

- Smart Switch para Mac descargado de Samsung oficial
- Binario analizado con `strings`, `file`, `7z`
- Comparación con análisis de Windows anterior

---

**Análisis completado**: 2025-12-27  
**Herramientas**: dmg2img, 7z, cpio, strings, file  
**Tamaño analizado**: 39 MB DMG → 156 MB descomprimido
