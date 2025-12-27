# Análisis de Autenticación y Descarga de Firmware Samsung

## Hallazgos del Error 403 Forbidden

### Servidor CDN Detectado
```
Server: AkamaiGHost
```

El servidor FOTA de Samsung (`fota-cloud-dn.ospserver.net`) está protegido por **Akamai CDN** con autenticación avanzada.

## Análisis de libdprw.so

### Funciones JNI Encontradas
```
Java_com_samsung_android_fotaagent_common_util_NativeUtils_unscramble
Java_com_samsung_android_fotaagent_common_util_NativeUtils_getKey
Java_com_samsung_android_fotaagent_common_util_NativeUtils_getRegiKey
Java_com_samsung_android_fotaagent_common_util_NativeUtils_getRegiValue
Java_com_samsung_android_fotaagent_common_util_NativeUtils_getTimeKey
Java_com_samsung_android_fotaagent_common_util_NativeUtils_getTimeValue
Java_com_samsung_android_fotaagent_common_util_NativeUtils_setPinAndFallocate
```

### Claves de Encriptación Extraídas
```
2cbmvps5z4
j5p7ll8g33
5763D0052DC1462E13751F753384E9A9
AF87056C54E8BFD81142D235F4F8E552
dkaghghkehlsvkdlsmld
```

### Archivos Importantes
```
/cache/checkp
```

## Métodos de Autenticación Posibles

### 1. Token de Akamai
Akamai CDN típicamente usa:
- **Auth token** en URL: `?__token__=exp=...~acl=...~hmac=...`
- **Cookie de autenticación**: Headers con firma HMAC
- **IP whitelisting**: Solo ciertos rangos de IP permitidos

### 2. Firma de Dispositivo
Basado en funciones nativas encontradas, posible firma compuesta por:
```python
signature = HMAC(
    key = getKey() + getRegiKey() + getTimeKey(),
    message = IMEI + MODEL + CSC + BOOT_ID + UFS_UN + timestamp
)
```

### 3. Proceso de Obtención del Token

#### Opción A: Via SOAgent76 + Samsung IDP
```
1. Autenticarse en Samsung IDP
   POST https://api.samsungidp.com/auth
   
2. Obtener device token
   POST https://dir-apis.samsungdm.com/api/v1/new/device
   Headers: Authorization: Bearer {idp_token}
   
3. Solicitar URL firmada
   POST https://dir-apis.samsungdm.com/api/v1/device/firmware/download
   Body: {model, csc, version, device_token}
   Response: {signed_url: "https://fota-cloud-dn.ospserver.net/...?__token__=..."}
```

#### Opción B: Via FUS Server
```
1. getNonce
   POST http://fus2.shop.v-cdn.net/FUS2/getNonce
   
2. getVersionLists (con auth HMAC-SHA1)
   
3. getBinaryInform
   Response incluye URL firmada con token
   
4. getBinaryFile con token
```

## Análisis de Otras Librerías

### libupdateprof.qti.so
- **Propósito**: Perfiles de actualización Qualcomm
- **Funciones**: `update_profiles`, `update_profiles_logs`
- **Relevancia**: No relacionada con autenticación de descarga

### libappfuse.so / libfuse_rust.dylib.so
- **Propósito**: Filesystem FUSE para Android
- **Relevancia**: Usado para montar OTA durante instalación, no para descarga

### librerias fusion (camera)
- **Propósito**: Procesamiento de imágenes de cámara
- **Relevancia**: No relacionadas con FOTA

## Estructura del URL de Descarga

### Formato Observado
```
https://fota-cloud-dn.ospserver.net/firmware/{CSC}/{MODEL}/{archivo}
```

### Posibles Nombres de Archivo
1. `update.zip` - OTA para adb sideload
2. `{MODEL}_{VERSION}.zip` - Firmware específico
3. `nspx/{hash}.zip` - Con hash específico
4. `{PATH_FROM_API}/{FILENAME}` - Path dinámico del API

### Tokens de Akamai
Los tokens típicamente tienen formato:
```
?__token__=exp={timestamp}~acl={path}~hmac={signature}
```

Donde:
- `exp`: Unix timestamp de expiración
- `acl`: Access Control List (path permitido)
- `hmac`: Firma HMAC-SHA256 del token

## Soluciones Propuestas

### Solución 1: Usar Servidor FUS Completo
El servidor FUS (`fus2.shop.v-cdn.net`) puede proporcionar URLs firmadas:

```python
# Obtener nonce
nonce = get_nonce()

# Autenticar
auth = HMAC_SHA1(nonce, IMEI + MODEL + CSC)

# Obtener binary info (incluye URL con token)
binary_info = get_binary_inform(auth)

# URL firmada en binary_info['url'] o binary_info['path']
download_url = binary_info['download_url']  # Ya incluye token
```

**Problema**: Servidor FUS no resuelve DNS en este entorno (posible bloqueo regional).

### Solución 2: Emular Samsung IDP + Device Management
```python
# 1. Autenticación IDP
idp_token = authenticate_samsung_idp()

# 2. Registrar dispositivo
device_token = register_device(idp_token, {
    'model': MODEL,
    'imei': IMEI,
    'boot_id': BOOT_ID,
    'ufs_un': UFS_UN
})

# 3. Solicitar URL de descarga firmada
signed_url = request_firmware_url(device_token, {
    'model': MODEL,
    'csc': CSC,
    'version': VERSION
})

# 4. Descargar con URL firmada
download(signed_url)
```

**Problema**: Requiere credenciales de Samsung Account o device attestation.

### Solución 3: Generar Token Akamai Manualmente
Si conocemos la clave secreta de Akamai:

```python
import hmac
import hashlib
import time

def generate_akamai_token(secret_key, path, expire_time):
    acl = path
    exp = int(time.time()) + expire_time
    
    # Construir auth string
    auth_string = f"exp={exp}~acl={acl}"
    
    # Generar HMAC
    h = hmac.new(
        secret_key.encode(),
        auth_string.encode(),
        hashlib.sha256
    )
    
    # Construir token
    token = f"{auth_string}~hmac={h.hexdigest()}"
    return token

# Usar token en URL
url = f"https://fota-cloud-dn.ospserver.net/firmware/TPA/SM-S916B/update.zip?__token__={token}"
```

**Problema**: No conocemos la clave secreta de Akamai (está en servidor Samsung, no en APK).

## Recomendaciones

### Opción Más Viable: Proxy/Interceptar Tráfico Real

1. **Usar dispositivo Android real** con FotaAgent
2. **Interceptar tráfico HTTPS** con mitmproxy/Burp Suite
3. **Capturar URL firmada** cuando FotaAgent descarga
4. **Analizar estructura del token** y cómo se genera

### Pasos:
```bash
# En PC con mitmproxy
mitmproxy --ssl-insecure

# En dispositivo Android
# 1. Instalar certificado mitmproxy
# 2. Configurar proxy
# 3. Abrir FotaAgent
# 4. Iniciar descarga de actualización
# 5. Capturar request con token
```

### Alternativa: Usar Smart Switch
Smart Switch (aplicación de escritorio de Samsung) descarga firmwares sin estas restricciones:
- No usa Akamai con autenticación estricta
- Usa servidores diferentes o con autenticación más simple
- Posiblemente usa FUS o servidores de desarrollo

## Conclusión

El error 403 Forbidden es causado por:
1. **Protección Akamai CDN** - Requiere token en URL
2. **Token dinámico** - Generado por servidor Samsung (FUS o DM API)
3. **No disponible en APK** - La clave para generar tokens está en servidor

**Para descarga exitosa se necesita**:
- Implementar flujo completo via FUS (si el servidor responde)
- O implementar autenticación via Samsung IDP + DM API
- O interceptar token de dispositivo real
- O usar herramienta alternativa como Smart Switch / Frija / Bifrost

## Próximos Pasos

1. ✅ Intentar FUS completo (si servidor responde)
2. ✅ Implementar Samsung IDP auth flow
3. ✅ Documentar cómo interceptar tráfico real
4. ✅ Crear script que funcione con tokens capturados manualmente
